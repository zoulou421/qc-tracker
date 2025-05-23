# -*- coding: utf-8 -*-
from odoo import models, fields


class QCTrackerDomainProject(models.Model):
    _name = 'qctracker.domain.project'
    _description = 'Domain Project'

    name = fields.Char(string='Domain', required=True, help='e.g., PS: SUPPORT')
