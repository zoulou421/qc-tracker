# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Task(models.Model):
    _name = 'qctracker.task'
    _description = 'A Task belongs to a Project and is assigned to an Employee'

    name = fields.Char(string='Name', required=True)
    process = fields.Char(string='Process')
    sub_process = fields.Char(string='Sub Process')
    employee_id = fields.Many2one('qctracker.employee', string='Assigned Employee')
    project_id = fields.Many2one('qctracker.project', string='Project')
    manager_id = fields.Many2one('qctracker.employee', string='Manager')
    start_date = fields.Date(string='Start Date')
    expected_end_date = fields.Date(string='Expected End Date')
    end_date = fields.Date(string='End Date')
    # ajout du champ pour gestion barre progression
    # ajout priorités
