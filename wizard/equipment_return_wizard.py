from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError


class EquipmentReturnWizard(models.TransientModel):
    _name = "equipment.return.wizard"
    _description = "Assistant de retour d'équipement"

    equipment_id = fields.Many2one("gestion.equipement", string="Équipement", required=True, readonly=True)
    employee_id = fields.Many2one("gestion.employee", string="Employé (actuel)", readonly=True, compute="_compute_employee_id")
    return_date = fields.Datetime(string="Date de retour", default=fields.Datetime.now, required=True)

    return_condition = fields.Selection(
        [("good", "Bon état"), ("damaged", "Endommagé"), ("lost", "Perdu")],
        default="good",
        required=True,
    )

    damage_description = fields.Text(string="Description des dommages")
    note = fields.Text(string="Note")

    @api.depends("equipment_id")
    def _compute_employee_id(self):
        for record in self:
            record.employee_id = record.equipment_id.employee_id

    @api.constrains("return_condition", "damage_description")
    def _check_damage_description(self):
        for rec in self:
            if rec.return_condition == "damaged" and not (rec.damage_description or "").strip():
                raise ValidationError("Veuillez décrire les dommages (obligatoire si endommagé).")

    def action_apply(self):
        self.ensure_one()
        equipment = self.equipment_id
        employee = self.employee_id

        if not employee:
            raise UserError("Cet équipement n'est pas assigné à un employé.")

        active_line = self.env["gestion.assignment.history"].search(
            [("equipment_id", "=", equipment.id), ("date_to", "=", False)],
            limit=1,
        )
        if not active_line:
            raise ValidationError("Aucune affectation active trouvée pour cet équipement.")

        extra = [f"Retour: {self.return_condition}"]
        if self.return_condition == "damaged":
            extra.append(f"Dommages: {self.damage_description}")
        if self.note:
            extra.append(f"Note: {self.note}")

        active_line.write({
            "date_to": self.return_date,
            "state": "returned",
            "note": ((active_line.note or "") + "\n" + "\n".join(extra)).strip(),
        })

        new_status = "disponible"
        if self.return_condition == "damaged":
            new_status = "reparation"
        elif self.return_condition == "lost":
            new_status = "retire"

        equipment.write({"employee_id": False, "statut": new_status})
        return {"type": "ir.actions.act_window_close"}