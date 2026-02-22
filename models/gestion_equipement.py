from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date


class GestionEquipementType(models.Model):
    _name = "gestion.equipement.type"
    _description = "Type d'Équipement"
    _rec_name = "name"

    name = fields.Char(string="Type", required=True, index=True)
    description = fields.Text(string="Description")

    _sql_constraints = [
        ("name_unique", "unique(name)", "Le type d'équipement doit être unique."),
    ]


class GestionEquipement(models.Model):
    _name = "gestion.equipement"
    _description = "Équipement"
    _rec_name = "nom"
    _order = "id desc"

    nom = fields.Char(string="Nom", required=True)
    numero_serie = fields.Char(string="Numéro de série", required=True, index=True)
    type = fields.Many2one("gestion.equipement.type", string="Type", required=True)
    date_achat = fields.Date(string="Date d'achat")
    date_expiration_garantie = fields.Date(string="Date d'expiration de garantie")

    statut = fields.Selection(
        [
            ("disponible", "Disponible"),
            ("assigne", "Assigné"),
            ("reparation", "En réparation"),
            ("retire", "Retiré"),
        ],
        string="Statut",
        default="disponible",
        required=True,
    )

    employee_id = fields.Many2one(
        "gestion.employee",
        string="Employé Assigné",
        ondelete="set null",  # avoids FK delete issues
    )

    image = fields.Image(string="Image de l'équipement")

    garantie_status = fields.Selection(
        [
            ("none", "Non renseignée"),
            ("valid", "Valide"),
            ("expiring_soon", "Expire bientôt"),
            ("expired", "Expirée"),
        ],
        string="État de la Garantie",
        compute="_compute_garantie_status",
        store=True,
    )
    garantie_days_left = fields.Integer(
        string="Jours restants",
        compute="_compute_garantie_status",
        store=True,
    )

    _sql_constraints = [
        ("numero_serie_unique", "unique(numero_serie)", "Le numéro de série doit être unique!"),
    ]

    @api.constrains("numero_serie")
    def _check_numero_serie_unique(self):
        for record in self:
            if record.numero_serie:
                existing = self.search(
                    [("numero_serie", "=", record.numero_serie), ("id", "!=", record.id)],
                    limit=1,
                )
                if existing:
                    raise ValidationError(
                        f"Le numéro de série '{record.numero_serie}' existe déjà. "
                        "Veuillez utiliser un numéro unique."
                    )

    @api.depends("date_expiration_garantie")
    def _compute_garantie_status(self):
        today = date.today()
        for record in self:
            if not record.date_expiration_garantie:
                record.garantie_status = "none"
                record.garantie_days_left = 0
                continue

            days_left = (record.date_expiration_garantie - today).days
            record.garantie_days_left = days_left

            if days_left < 0:
                record.garantie_status = "expired"
            elif days_left < 30:
                record.garantie_status = "expiring_soon"
            else:
                record.garantie_status = "valid"

    @api.constrains("statut", "employee_id")
    def _check_status_employee_consistency(self):
        for record in self:
            if record.employee_id and record.statut != "assigne":
                raise ValidationError("Si un employé est assigné, le statut doit être 'Assigné'.")
            if record.statut == "assigne" and not record.employee_id:
                raise ValidationError("Si le statut est 'Assigné', vous devez choisir un employé.")

    def action_open_assign_wizard(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Assigner / Transférer",
            "res_model": "equipment.assignment.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {"default_equipment_id": self.id},
        }

    def action_open_return_wizard(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Retourner",
            "res_model": "equipment.return.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {"default_equipment_id": self.id},
        }

    def action_back_to_kanban(self):
        """Navigate back to equipment kanban view"""
        return {
            "type": "ir.actions.act_window",
            "name": "Équipements",
            "res_model": "gestion.equipement",
            "view_mode": "kanban,tree,form",
            "target": "current",
        }