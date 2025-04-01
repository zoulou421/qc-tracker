# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError

class QCTrackerTask(models.Model):
    _name = 'qctracker.task'
    _description = 'A Task belongs to a Project and is assigned to an Employee'

    name = fields.Char(string='Task Name', required=True)
    process = fields.Char(string='Process')
    sub_process = fields.Char(string='Sub Process')
    employee_id = fields.Many2one('qctracker.employee', string='Assigned Employee')
    project_id = fields.Many2one('qctracker.project', string='Project')
    manager_id = fields.Many2one('qctracker.employee', string='Manager')
    start_date = fields.Date(string='Start Date')
    expected_end_date = fields.Date(string='Expected End Date')
    end_date = fields.Date(string='End Date')

    # Champ de progression
    progress = fields.Float(string='Progress', default=0.0, help="Progress of the task in percentage", digits=(6, 2))

    # Ajout des priorités
    priority = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High')
    ], string='Priority', default='medium')

    # Fonction pour envoyer une notification par e-mail
    def send_task_notification(self):
        for task in self:
            # Vérifier si un employé est affecté et un manager est défini
            if task.employee_id and task.manager_id:
                template = self.env.ref('qc_tracker.email_template_task_notification')
                if not template:
                    raise UserError("Template not found.")
                # Envoi de l'email via le template
                template.send_mail(task.id, force_send=True)
