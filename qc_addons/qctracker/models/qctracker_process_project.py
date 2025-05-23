# -*- coding: utf-8 -*-
from odoo import models, fields


class QCTrackerProcessProject(models.Model):
    _name = 'qctracker.process.project'
    _description = 'Process Project'

    name = fields.Char(string='Process', required=True, help='e.g., PS4. Information system management')
    domain_id = fields.Many2one('qctracker.domain.project', string='Domain', required=True, ondelete='cascade')
