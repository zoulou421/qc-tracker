# -*- coding: utf-8 -*-

from odoo import models, fields, api


class QCTrackerSubTask(models.Model):
    _name = 'qctracker.subtask'
    _description = 'A Sub_Task depends on a Task'

    task_id = fields.Many2one('qctracker.task', string='Task')
    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    employee_id = fields.Many2one('qctracker.employee', string='Assigned Employee')
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    status = fields.Selection([('in_progress', 'In Progress'), ('completed', 'Completed')], string='Status')


