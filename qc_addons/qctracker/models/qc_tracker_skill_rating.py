# -*- coding: utf-8 -*-

from odoo import models, fields, api


class QCTrackerSkillRating(models.Model):
    """Model for detailed skill ratings within employee evaluations."""
    _name = 'qctracker.skillrating'
    _description = 'Skill Rating in Evaluation'

    rating_id = fields.Many2one(
        'qctracker.employeerating',
        string='Evaluation',
        required=True,  # Make this required
        ondelete='cascade'  # Add cascade deletion
    )
    skill_id = fields.Many2one('qctracker.skill', string='Skill', required=True)
    rating = fields.Selection([
        ('1', 'Basic'),
        ('2', 'Intermediate'),
        ('3', 'Advanced'),
        ('4', 'Expert')
    ], string='Rating', required=True)
    comments = fields.Text(string='Comments')