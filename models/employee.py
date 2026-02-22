from odoo import models, fields, api


class GestionEmployee(models.Model):
    _name = "gestion.employee"
    _description = "Employé"
    _order = "name"

    name = fields.Char(string="Nom complet", required=True)
    matricule = fields.Char(string="Matricule", required=True, index=True)
    email = fields.Char(string="Email")
    phone = fields.Char(string="Téléphone")

    department_id = fields.Many2one("gestion.department", string="Département")
    job_title = fields.Char(string="Poste")
    manager_id = fields.Many2one("gestion.employee", string="Manager", ondelete="set null")

    active = fields.Boolean(default=True)
    image = fields.Image(string="Photo de profil")

    equipment_ids = fields.One2many("gestion.equipement", "employee_id", string="Équipements assignés")
    assignment_history_ids = fields.One2many("gestion.assignment.history", "employee_id", string="Historique des affectations")

    equipment_count = fields.Integer(compute="_compute_equipment_count", string="Nombre d'équipements")

    @api.depends("equipment_ids")
    def _compute_equipment_count(self):
        for rec in self:
            rec.equipment_count = len(rec.equipment_ids)

    _sql_constraints = [
        ("matricule_unique", "unique(matricule)", "Le matricule doit être unique."),
    ]

    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, f"{record.name} ({record.matricule})"))
        return result

    def action_view_equipment(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": f"Équipements de {self.name}",
            "res_model": "gestion.equipement",
            "view_mode": "tree,form",
            "domain": [("employee_id", "=", self.id)],
            "context": {"default_employee_id": self.id},
        }

    def action_back_to_kanban(self):
        return {
            "type": "ir.actions.act_window",
            "res_model": "gestion.employee",
            "view_mode": "kanban",
            "views": [(False, "kanban")],
            "target": "current",
        }