# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

class QCTrackerProcess(models.Model):
    """
    Modèle Odoo représentant un processus principal.
    Permet de définir les étapes générales dans le suivi des tâches.
    """
    _name = 'qctracker.process'
    name = fields.Char('Nom du Processus')

class QCTrackerSubProcess(models.Model):
    """
    Modèle Odoo représentant un sous-processus.
    Permet de définir les sous-processus associés à un processus principal.
    """
    _name = 'qctracker.sub.process'
    name = fields.Char('Nom du Sous-Processus')
    process_id = fields.Many2one('qctracker.process', 'Processus')

class QCTrackerTask(models.Model):
    """
    Modèle Odoo représentant une tâche.
    Une tâche appartient à un projet et est assignée à un employé.
    """
    _name = 'qctracker.task'
    _description = 'Une tâche appartient à un projet et est assignée à un employé'

    name = fields.Char(string='Nom de la Tâche', required=True)
    description = fields.Char(string='Description de la Tâche')
    process_id = fields.Many2one('qctracker.process', string='Processus')
    sub_process_id = fields.Many2one('qctracker.sub.process', string='Sous-Processus', domain="[('process_id', '=', process_id)]")
    employee_id = fields.Many2one('qctracker.employee', string='Employé Assigné')
    project_id = fields.Many2one('qctracker.project', string='Projet')
    manager_id = fields.Many2one('qctracker.employee', string='Responsable')
    start_date = fields.Date(string='Date de Début')
    expected_end_date = fields.Date(string='Date de Fin Prévue')
    end_date = fields.Date(string='Date de Fin Réelle')
    progress = fields.Float(string='Progression', default=0.0, help="Progression de la tâche en pourcentage", digits=(6, 2))
    priority = fields.Selection([('low', 'Basse'), ('medium', 'Moyenne'), ('high', 'Haute')], string='Priorité', default='medium')
    subtask_ids = fields.One2many('qctracker.subtask', 'task_id', string='Sous-Tâches')
    status = fields.Selection([('to_do', 'À Faire'), ('in_progress', 'En Cours'), ('done', 'Terminée')], string='Statut', default='to_do', help='Statut de la tâche')

    @api.constrains('start_date', 'expected_end_date', 'end_date')
    def _check_dates(self):
        """
        Vérifie que la date de début est antérieure aux dates de fin prévue et réelle.
        """
        for task in self:
            if task.start_date and task.expected_end_date and task.start_date > task.expected_end_date:
                raise ValidationError("La date de début doit être antérieure à la date de fin prévue.")
            if task.start_date and task.end_date and task.start_date > task.end_date:
                raise ValidationError("La date de début doit être antérieure à la date de fin réelle.")

    def send_task_notification(self):
        """
        Envoie une notification par e-mail à l'employé et au responsable de la tâche.
        Utilise un modèle d'e-mail défini dans Odoo.
        Lève une exception UserError si le modèle d'e-mail n'est pas trouvé.
        """
        for task in self:
            if task.employee_id and task.manager_id:
                template = self.env.ref('qc_tracker.email_template_task_notification', raise_if_not_found=False)
                if template:
                    template.send_mail(task.id, force_send=True)
                else:
                    raise UserError("Le modèle d'e-mail 'qc_tracker.email_template_task_notification' est introuvable.")