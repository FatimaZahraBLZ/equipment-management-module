from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError


class EquipmentAssignmentWizard(models.TransientModel):
    _name = "equipment.assignment.wizard"
    _description = "Assistant d'assignation / transfert d'équipement"

    equipment_id = fields.Many2one("gestion.equipement", string="Équipement", required=True, readonly=True)
    employee_id = fields.Many2one("gestion.employee", string="Employé", required=True)
    assignment_date = fields.Datetime(string="Date", default=fields.Datetime.now, required=True)
    note = fields.Text(string="Note")
    action_type = fields.Selection([("assign", "Assigner"), ("transfer", "Transférer")], default="assign", required=True)

    @api.onchange("action_type")
    def _onchange_action_type(self):
        if self.action_type == "transfer" and not self.note:
            self.note = "Transfert d'équipement"

    def action_apply(self):
        self.ensure_one()

        equipment = self.equipment_id
        new_employee = self.employee_id
        old_employee = equipment.employee_id

        if equipment.statut == "retire":
            raise UserError("Impossible d'assigner un équipement retiré.")

        if self.action_type == "assign" and old_employee:
            raise ValidationError(
                f"Cet équipement est déjà assigné à {old_employee.name}. "
                "Choisissez 'Transférer' pour changer l'employé."
            )

        if self.action_type == "transfer" and old_employee == new_employee:
            raise ValidationError("Impossible de transférer l'équipement au même employé.")

        active_line = self.env["gestion.assignment.history"].search(
            [("equipment_id", "=", equipment.id), ("date_to", "=", False)],
            limit=1,
        )
        if active_line:
            active_line.write({"date_to": self.assignment_date, "state": "transfer"})

        self.env["gestion.assignment.history"].create({
            "equipment_id": equipment.id,
            "employee_id": new_employee.id,
            "date_from": self.assignment_date,
            "date_to": False,
            "assigned_by": self.env.user.id,
            "state": "active",
            "note": self.note or "Assignation via assistant",
        })

        equipment.write({"employee_id": new_employee.id, "statut": "assigne"})
        return {"type": "ir.actions.act_window_close"}