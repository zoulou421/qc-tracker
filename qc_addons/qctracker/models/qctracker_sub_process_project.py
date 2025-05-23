# -*- coding: utf-8 -*-
from odoo import models, fields


class QCTrackerSubProcess(models.Model):
    _name = 'qctracker.sub_process.project'
    _description = 'Sub Process Project'

    name = fields.Char(string='Sub Process', required=True, help='e.g., PS4.1: Manage IT and office equipment')
    process_id = fields.Many2one('qctracker.process.project', string='Process', required=True, ondelete='cascade')
