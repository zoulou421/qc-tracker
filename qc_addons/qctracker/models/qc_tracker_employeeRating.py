# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class QCTrackerEmployeeRating(models.Model):
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
    state = fields.Selection([('draft', 'Draft'), ('submitted', 'Submitted')], default='draft', string='State')

    @api.model  # Replacing @api.multi with @api.model
    def action_submit(self):
        """
        Submit the employee rating, marking it as 'submitted'.
        """
        for record in self:
            # Ensure that all necessary fields are filled before submitting
            if not record.rating:
                raise ValidationError("Please provide a rating before submitting.")
            if not record.evaluation_date:
                raise ValidationError("Please provide an evaluation date before submitting.")

            # Mark the record as submitted
            record.state = 'submitted'
        return True

    @api.model  # Replacing @api.multi with @api.model
    def action_reset(self):
        """
        Reset the rating fields and change state to 'draft'.
        """
        for record in self:
            # Reset fields to initial state
            record.rating = False
            record.on_time = False
            record.comments = False
            record.evaluation_date = False
            record.state = 'draft'
        return True
