# -*- coding: utf-8 -*-
from odoo import models, fields

class QCTrackerSubProcess(models.Model):
    _name = 'qctracker.sub.process'
    _description = 'Sous-processus'

    name = fields.Char(string='Nom du Sous-Processus')
    process_id = fields.Many2one('qctracker.process', string='Processus')