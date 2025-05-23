# --- QCTrackerTag Model ---
from odoo import models, fields


class QCTrackerTag(models.Model):
    """
    Modèle Odoo représentant un tag de projet.
    """
    _name = "qctracker.tag"
    _description = "Project Tags"

    name = fields.Char(string="Tag Name", required=True)