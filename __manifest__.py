{
    "name": "Gestion des Équipements",
    "author": "Fatima Ezzahra BOULOUIZ",
    "version": "1.1",
    "category": "Operations",
    "summary": "Gestion des équipements + employés (custom) + historique d'affectation",
    "depends": ["base"],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",

        "views/gestion_equipement_views.xml",
        "views/employee_views.xml",
        "views/assignment_history_views.xml",
        "views/department_views.xml",
        "views/wizard_views.xml",
        "views/menus.xml",
    ],
    "application": True,
    "installable": True,
}