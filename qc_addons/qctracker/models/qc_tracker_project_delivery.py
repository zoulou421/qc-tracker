# -*- coding: utf-8 -*-

from odoo import models, fields, api

class QCTrackerProjectDelivery(models.Model):
    _name = 'qctracker.projectdelivery'
    _description = 'A Project_Delivery is validated by a Manager'

    project_id = fields.Many2one('qctracker.project', string='Project')
    manager_id = fields.Many2one('qctracker.employee', string='Manager')
    on_time = fields.Boolean(string='On Time')
    comments = fields.Text(string='Comments')
    delivery_date = fields.Date(string='Delivery Date')