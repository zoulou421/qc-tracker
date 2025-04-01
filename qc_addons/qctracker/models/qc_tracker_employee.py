# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, AccessError, UserError
from datetime import datetime, timedelta

class QCTrackerEmployee(models.Model):
    #_inherit = 'employee.transfer'  # Inherit from EmployeeTransfer model
    _inherit = 'employee.transfer'
    _name = 'qctracker.employee'
    _description = 'An Employee can belong to a Department and be a Manager'

    # Fields specific to QCTrackerEmployee
    # name = fields.Char(string='Name', required=True)
    name = fields.Char(string='Full Name', compute='_compute_full_name', store=True)
    last_name = fields.Char(string='First Name', required=True)
    first_name = fields.Char(string='Last Name', required=True)
    email = fields.Char(string='Email', required=True)
    phone = fields.Char(string='Phone')
    # role = fields.Char(string='Role')
    role = fields.Selection([
        ('employee', 'Employee'),
        ('manager', 'Manager'),
        ('admin', 'Admin')
    ], string='Role', required=True)
    department_id = fields.Many2one('qctracker.department', string='Department')
    # is_manager = fields.Boolean(string='Is Manager', default=False)
    is_manager = fields.Boolean(string='Is Manager', compute='_compute_is_manager', store=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string='Gender')
    country = fields.Char(string='Country')

    # Computed field to combine first and last name into a full name
    @api.depends('first_name', 'last_name')
    def _compute_full_name(self):
        for rec in self:
            rec.name = f"{rec.first_name} {rec.last_name}" if rec.first_name and rec.last_name else ''

    @api.depends('role')
    def _compute_is_manager(self):
        for rec in self:
            rec.is_manager = rec.role == 'manager'