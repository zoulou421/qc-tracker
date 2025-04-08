# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class QCTrackerProcess(models.Model):
    """
    Modèle Odoo représentant un processus principal.

    Ce modèle permet de définir les étapes générales dans le suivi des tâches.
    Chaque processus principal peut avoir plusieurs sous-processus associés.

    Champs :
        - name (Char) : Nom du processus principal.
    """
    _name = 'qctracker.process'
    name = fields.Char('Nom du Processus')


class QCTrackerSubProcess(models.Model):
    """
    Modèle Odoo représentant un sous-processus.

    Ce modèle permet de définir les sous-processus associés à un processus principal.
    Un sous-processus appartient toujours à un processus principal.

    Champs :
        - name (Char) : Nom du sous-processus.
        - process_id (Many2one) : Relation vers le processus principal auquel appartient ce sous-processus.
    """
    _name = 'qctracker.sub.process'
    name = fields.Char('Nom du Sous-Processus')
    process_id = fields.Many2one('qctracker.process', 'Processus')


class QCTrackerTask(models.Model):
    """
    Modèle Odoo représentant une tâche.

    Une tâche appartient à un projet et est assignée à un employé.
    Ce modèle permet de suivre les détails d'une tâche, son statut, sa progression, etc.

    Champs :
        - name (Char) : Nom de la tâche (obligatoire).
        - description (Char) : Description de la tâche.
        - process_id (Many2one) : Relation vers le processus principal associé à la tâche.
        - sub_process_id (Many2one) : Relation vers le sous-processus associé à la tâche.
        - employee_id (Many2one) : Relation vers l'employé assigné à la tâche.
        - project_id (Many2one) : Relation vers le projet auquel appartient la tâche.
        - manager_id (Many2one) : Relation vers le responsable de la tâche.
        - start_date (Date) : Date de début de la tâche.
        - expected_end_date (Date) : Date de fin prévue de la tâche.
        - end_date (Date) : Date de fin réelle de la tâche.
        - progress (Float) : Progression de la tâche en pourcentage (par défaut 0.0).
        - priority (Selection) : Priorité de la tâche (basse, moyenne, haute).
        - subtask_ids (One2many) : Relation vers les sous-tâches associées à cette tâche.
        - status (Selection) : Statut de la tâche (à faire, en cours, terminée).

    Contraintes :
        - _check_dates() : Vérifie que la date de début est antérieure aux dates de fin prévue et réelle.

    Méthodes :
        - send_task_notification() : Envoie une notification par e-mail à l'employé et au responsable de la tâche.
    """
    _name = 'qctracker.task'
    _inherit = ['mail.thread', 'mail.activity.mixin'] # Add this line
    _description = 'Une tâche appartient à un projet et est assignée à un employé'

    name = fields.Char(string='Nom de la Tâche', required=True)
    description = fields.Char(string='Description de la Tâche')
    process_id = fields.Many2one('qctracker.process', string='Processus')
    sub_process_id = fields.Many2one('qctracker.sub.process', string='Sous-Processus',
                                     domain="[('process_id', '=', process_id)]")
    employee_id = fields.Many2one('qctracker.employee', string='Employé Assigné')
    project_id = fields.Many2one('qctracker.project', string='Projet')
    manager_id = fields.Many2one('qctracker.employee', string='Responsable')
    start_date = fields.Date(string='Date de Début')
    expected_end_date = fields.Date(string='Date de Fin Prévue')
    end_date = fields.Date(string='Date de Fin Réelle')
    progress = fields.Float(string='Progression', default=0.0, help="Progression de la tâche en pourcentage",
                            digits=(6, 2))
    priority = fields.Selection([('low', 'Basse'), ('medium', 'Moyenne'), ('high', 'Haute')], string='Priorité',
                                default='medium')
    subtask_ids = fields.One2many('qctracker.subtask', 'task_id', string='Sous-Tâches')
    status = fields.Selection([('to_do', 'À Faire'), ('in_progress', 'En Cours'), ('done', 'Terminée')],
                              string='Statut', default='to_do', help='Statut de la tâche')

    @api.constrains('start_date', 'expected_end_date', 'end_date')
    def _check_dates(self):
        """
        Vérifie que la date de début est antérieure aux dates de fin prévue et réelle.

        Lève une exception ValidationError si la date de début est postérieure à l'une des dates de fin.
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
