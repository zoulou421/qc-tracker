# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

"""
=========Objectif====== :
Ce modèle représente un projet au sein de votre application Odoo.
Il permet de gérer les informations relatives aux projets, tels que leur nom, leur description, leur département associé, leurs dates de début et de fin, leur manager, leurs tâches associées, leur statut et leur progression.

========Champs======== :
name (Char, obligatoire) : Le nom du projet.
description (Text) : La description du projet.
department_id (Many2one vers qctracker.department) : Le département auquel le projet est associé.
start_date (Date) : La date de début du projet.
end_date (Date) : La date de fin du projet.
manager_id (Many2one vers qctracker.employee) : Le manager du projet.
task_ids (One2many vers qctracker.task) : Les tâches associées au projet.
status (Selection, par défaut 'to_do') : Le statut du projet (to_do, in_progress, done).
progress (Integer, calculé et stocké) : La progression du projet en pourcentage.
tag_ids (Many2many vers qctracker.tag) : Les tags associés au projet.
project_delivery_ids (One2many vers qctracker.projectdelivery) : les livraisons de projet associées.

========Méthodes========= :
_check_dates() : Valide que la date de fin est postérieure à la date de début.
_compute_progress() : Calcule la progression du projet en fonction des statuts des tâches associées.

========Fonctionnalités Clés======= :
Gestion des informations de base des projets.
Association des projets aux départements et aux tâches.
Suivi du statut et de la progression des projets.
gestion des tags.
gestion des livraisons.
Validation des dates.

===========Utilisation========== :
Ce modèle est essentiel pour gérer les projets au sein de votre application Odoo.
Il permet de centraliser les informations relatives aux projets et de faciliter la gestion des projets.
"""


# --- QCTrackerProject Model ---
class QCTrackerProject(models.Model):
    """
    Modèle Odoo représentant un projet.
    Un projet est associé à un département et peut avoir plusieurs tâches.
    """
    _name = 'qctracker.project'
    _description = 'A Project is attached to a Department'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    department_id = fields.Many2one('qctracker.department', string='Department')
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    employee_id = fields.Many2one('qctracker.employee', string='Project Manager')
    task_ids = fields.One2many('qctracker.task', 'project_id', string='Tasks')
    status = fields.Selection([
        ('to_do', 'To Do'),
        ('in_progress', 'In Progress'),
        ('done', 'Completed'),
    ], string='Status', default='to_do', help='Task status')
    progress = fields.Integer(string="Progress", compute='_compute_progress',
                              store=True)  # Calcule auto de la progression
    tag_ids = fields.Many2many('qctracker.tag', string="Tags")

    project_delivery_ids = fields.One2many('qctracker.projectdelivery', 'project_id', string='Project Delivery')

    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        """
        Valide que la date de fin est postérieure à la date de début.
        """
        for record in self:
            if record.start_date and record.end_date and record.end_date < record.start_date:
                raise ValidationError("End date must be after start date.")

    @api.depends('task_ids.status')
    def _compute_progress(self):
        """
        Calcule la progression du projet en fonction des statuts des tâches associées.
        """
        for project in self:
            tasks = project.task_ids
            if tasks:
                completed_tasks = len(tasks.filtered(lambda t: t.status == 'done'))
                project.progress = int((completed_tasks / len(tasks)) * 100)
            else:
                project.progress = 0


# --- QCTrackerTag Model ---
class QCTrackerTag(models.Model):
    """
    Modèle Odoo représentant un tag de projet.
    """
    _name = "qctracker.tag"
    _description = "Project Tags"

    name = fields.Char(string="Tag Name", required=True)
