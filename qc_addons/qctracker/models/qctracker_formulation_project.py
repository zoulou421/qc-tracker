# -*- coding: utf-8 -*-
from odoo import models, fields


class QCTrackerTaskFormulationProject(models.Model):
    _name = 'qctracker.task_formulation.project'
    _description = 'Task Formulation Project'

    name = fields.Char(string='Task Formulation', required=True, help='e.g., Identify ICT equipment needs...')
    procedure_id = fields.Many2one('qctracker.procedure.project', string='Procedure', required=True, ondelete='cascade')
