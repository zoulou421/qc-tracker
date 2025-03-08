# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Project(models.Model):
    _name = 'qctracker.project'
    _description = 'A Project is attached to a Department'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    department_id = fields.Many2one('qctracker.department', string='Department')
    start_date = fields.Date(string='Start Date')
    expected_end_date = fields.Date(string='Expected End Date')
    end_date = fields.Date(string='End Date')
