# -*- coding: utf-8 -*-
from odoo import models, fields


class QCTrackerProcess(models.Model):
    _name = 'qctracker.process'
    _description = 'Processus principal'

    name = fields.Char(string='Nom du Processus')
