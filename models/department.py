from odoo import models, fields


class GestionDepartment(models.Model):
    _name = "gestion.department"
    _description = "Département"
    _order = "name"

    name = fields.Char(string="Nom", required=True)
    manager_id = fields.Many2one("gestion.employee", string="Manager")

    _sql_constraints = [
        ("name_unique", "unique(name)", "Le nom du département doit être unique."),
    ]

    def action_back_to_kanban(self):
        return {
            "type": "ir.actions.act_window",
            "res_model": "gestion.department",
            "view_mode": "kanban",
            "views": [(False, "kanban")],
            "target": "current",
        }