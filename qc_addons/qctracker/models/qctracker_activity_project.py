# -*- coding: utf-8 -*-
from odoo import models, fields


class QCTrackerActivityProject(models.Model):
    _name = 'qctracker.activity.project'
    _description = 'Activity Project'

    name = fields.Char(string='Activity', required=True, help='e.g., PS4.1_A1: Manage IT equipment inputs/outputs')
    sub_process_id = fields.Many2one('qctracker.sub_process.project', string='Sub Process', required=True, ondelete='cascade')
