# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Department(models.Model):
    _name = 'qctracker.department'
    _description = 'A Department has several Employees'

    name = fields.Char(string='Name', required=True)
    manager_id = fields.Many2one('qctracker.employee', string='Manager')
