from odoo import models, fields, api
from odoo.exceptions import ValidationError


class GestionAssignmentHistory(models.Model):
    _name = "gestion.assignment.history"
    _description = "Historique d'affectation"
    _order = "date_from desc"

    equipment_id = fields.Many2one("gestion.equipement", string="Équipement", required=True, ondelete="cascade")
    employee_id = fields.Many2one("gestion.employee", string="Employé", required=True, ondelete="restrict")

    date_from = fields.Datetime(string="Date de début", required=True, default=fields.Datetime.now)
    date_to = fields.Datetime(string="Date de fin")

    assigned_by = fields.Many2one("res.users", string="Assigné par", default=lambda self: self.env.user, readonly=True)
    note = fields.Text(string="Note")

    state = fields.Selection(
        [("active", "Actif"), ("returned", "Retourné"), ("transfer", "Transféré")],
        string="État",
        default="active",
        required=True,
    )

    @api.constrains("date_from", "date_to")
    def _check_dates(self):
        for rec in self:
            if rec.date_to and rec.date_to < rec.date_from:
                raise ValidationError("La date de fin ne peut pas être antérieure à la date de début.")

    @api.constrains("equipment_id", "date_to")
    def _check_single_active_assignment(self):
        for rec in self:
            if not rec.date_to:
                conflicting = self.search([
                    ("equipment_id", "=", rec.equipment_id.id),
                    ("date_to", "=", False),
                    ("id", "!=", rec.id),
                ])
                if conflicting:
                    raise ValidationError(f"L'équipement {rec.equipment_id.nom} a déjà une affectation active.")