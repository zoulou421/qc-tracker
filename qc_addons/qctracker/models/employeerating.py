# -*- coding: utf-8 -*-

from odoo import models, fields, api


class EmployeeRating(models.Model):
    _name = 'qctracker.employeerating'
    _description = 'An Employee_Rating is given by a Manager to evaluate an Employee'

    employee_id = fields.Many2one('qctracker.employee', string='Employee')
    project_id = fields.Many2one('qctracker.project', string='Project')
    manager_id = fields.Many2one('qctracker.employee', string='Manager')
    rating = fields.Selection([('1', 'Poor'), ('2', 'Fair'), ('3', 'Good'), ('4', 'Very Good'), ('5', 'Excellent')],
                              string='Rating')
    on_time = fields.Boolean(string='On Time')
    comments = fields.Text(string='Comments')
    evaluation_date = fields.Date(string='Evaluation Date')