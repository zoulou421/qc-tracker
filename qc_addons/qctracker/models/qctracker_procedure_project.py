# -*- coding: utf-8 -*-
from odoo import models, fields


class QCTrackerProcedureProject(models.Model):
    _name = 'qctracker.procedure.project'
    _description = 'Procedure Project'

    name = fields.Char(string='Procedure Project', required=True, help='e.g., PS4.1_A1_P1: Identify ICT equipment needs...')
    activity_id = fields.Many2one('qctracker.activity.project', string='Activity', required=True, ondelete='cascade')

