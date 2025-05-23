# -*- coding: utf-8 -*-

from odoo import models, fields, api


# --- QCTracker Category Model ---
class QCTrackerCategory(models.Model):
    _name = 'qctracker.category'
    _description = 'Project Category'

    name = fields.Char(string='Category Name', required=True)
    parent_id = fields.Many2one('qctracker.category', string='Parent Category', ondelete='cascade')
    child_ids = fields.One2many('qctracker.category', 'parent_id', string='Subcategories')
    display_name = fields.Char(string='Display Name', compute='_compute_display_name', store=True)
    display_name = fields.Char(
        string='Display Name',
        compute='_compute_display_name',
        store=True,
        recursive=True  # Add this to handle recursive computation
    )

    @api.depends('name', 'parent_id.display_name')
    def _compute_display_name(self):
        for category in self:
            if category.parent_id:
                category.display_name = f"{category.parent_id.display_name} / {category.name}"
            else:
                category.display_name = category.name
