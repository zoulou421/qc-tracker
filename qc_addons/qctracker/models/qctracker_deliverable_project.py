# -*- coding: utf-8 -*-
from odoo import models, fields


class QCTrackerDeliverableProject(models.Model):
    _name = 'qctracker.deliverable.project'
    _description = 'Deliverable Project'

    name = fields.Char(string='Deliverable Project', required=True, help='e.g., PS4.1_A1_L1: IT Asset Register')
    #livrable lié à l'activité. A modifier.
    procedure_id = fields.Many2one('qctracker.procedure.project', string='Procedure', required=True, ondelete='cascade')
