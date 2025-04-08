# -*- coding: utf-8 -*-

from odoo import models, fields, api
"""
===========Objectif========== :
Ce modèle représente une sous-tâche, qui est une étape plus petite et plus détaillée d'une tâche principale.
Il permet de décomposer les tâches complexes en sous-tâches plus gérables.

============Champs============== :
task_id (Many2one vers qctracker.task) : La tâche principale à laquelle la sous-tâche appartient.
name (Char, obligatoire) : Le nom de la sous-tâche.
description (Text) : La description détaillée de la sous-tâche.
employee_id (Many2one vers qctracker.employee) : L'employé assigné à la sous-tâche.
start_date (Date) : La date de début de la sous-tâche.
end_date (Date) : La date de fin de la sous-tâche.
status (Selection) : Le statut de la sous-tâche (En cours, Terminé).

===========Fonctionnalités Clés=========== :
Gestion des sous-tâches.
Association des sous-tâches aux tâches principales et aux employés.
Suivi des dates de début et de fin des sous-tâches.
Suivi du statut des sous-tâches.

===========Utilisation========= :
Ce modèle est utilisé pour décomposer les tâches complexes en étapes plus petites et plus gérables.
Il permet de suivre les progrès des sous-tâches et d'assurer une meilleure gestion des tâches.
"""

class QCTrackerSubTask(models.Model):
    """
    Modèle Odoo représentant une sous-tâche.
    Une sous-tâche dépend d'une tâche principale et est utilisée pour décomposer une tâche en étapes plus petites.
    """
    _name = 'qctracker.subtask'
    _description = 'A Sub_Task depends on a Task'

    task_id = fields.Many2one('qctracker.task', string='Task')
    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    # employee_id = fields.Many2one('qctracker.employee', string='Assigned Employee')
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    status = fields.Selection([('in_progress', 'In Progress'), ('completed', 'Completed')], string='Status')