# -*- coding: utf-8 -*-

from odoo import models, fields, api


class QCTrackerSkill(models.Model):
    """Model representing skills that employees can possess."""
    _name = 'qctracker.skill'
    _description = 'Employee Skill'

    name = fields.Char(string='Skill Name', required=True)
    description = fields.Text(string='Description')
    category = fields.Selection([
        ('technical', 'Technical'),
        ('soft', 'Soft Skills'),
        ('language', 'Language'),
        ('other', 'Other')
    ], string='Category')
    active = fields.Boolean(string='Active', default=True)