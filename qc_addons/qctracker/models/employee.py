# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Employee(models.Model):
    _name = 'qctracker.employee'
    _description = 'An Employee can belong to a Department and be a Manager'

    name = fields.Char(string='Name', required=True)
    first_name = fields.Char(string='First Name', required=True)
    email = fields.Char(string='Email', required=True)
    phone = fields.Char(string='Phone')
    role = fields.Char(string='Role')
    department_id = fields.Many2one('qctracker.department', string='Department')
    is_manager = fields.Boolean(string='Is Manager', default=False)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string='Gender')
    country = fields.Char(string='Country')