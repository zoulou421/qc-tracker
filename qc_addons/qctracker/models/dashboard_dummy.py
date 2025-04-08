from odoo import models, fields

class DashboardDummy(models.Model):
    _name = "dashboard.dummy"
    _description = "Dashboard Dummy"
    _auto = False  # Pas de table en BDD

    name = fields.Char(string="Nom")  # champ factice juste pour rassurer Odoo
