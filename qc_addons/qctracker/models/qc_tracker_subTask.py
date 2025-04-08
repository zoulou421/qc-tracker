# -*- coding: utf-8 -*-

from odoo import models, fields, api

class QCTrackerSubTask(models.Model):
    """
    Modèle Odoo représentant une sous-tâche.

    Objectif :
        Ce modèle représente une sous-tâche, qui est une étape plus petite et plus détaillée d'une tâche principale.
        Il permet de décomposer les tâches complexes en sous-tâches plus gérables.

    Champs :
        task_id (Many2one vers qctracker.task) :
            La tâche principale à laquelle la sous-tâche appartient.
            Ce champ établit une relation Many2one avec le modèle 'qctracker.task', permettant d'associer chaque sous-tâche à une tâche principale spécifique.

        name (Char, obligatoire) :
            Le nom de la sous-tâche.
            Ce champ est obligatoire et stocke le nom de la sous-tâche.

        description (Text) :
            La description détaillée de la sous-tâche.
            Ce champ stocke une description textuelle détaillée de la sous-tâche, fournissant des informations supplémentaires sur ce qu'elle implique.

        start_date (Date) :
            La date de début de la sous-tâche.
            Ce champ stocke la date à laquelle la sous-tâche doit commencer.

        end_date (Date) :
            La date de fin de la sous-tâche.
            Ce champ stocke la date à laquelle la sous-tâche doit être terminée.

        status (Selection) :
            Le statut de la sous-tâche (En cours, Terminé).
            Ce champ stocke le statut actuel de la sous-tâche, permettant de suivre sa progression.
            Les options de statut sont 'in_progress' (En cours) et 'completed' (Terminé).

    Fonctionnalités Clés :
        - Gestion des sous-tâches : Permet de créer, modifier et supprimer des sous-tâches.
        - Association des sous-tâches aux tâches principales : Établit une relation claire entre les sous-tâches et leurs tâches principales.
        - Suivi des dates de début et de fin des sous-tâches : Permet de planifier et de suivre les échéances des sous-tâches.
        - Suivi du statut des sous-tâches : Permet de suivre la progression des sous-tâches et de s'assurer qu'elles sont terminées à temps.

    Utilisation :
        Ce modèle est utilisé pour décomposer les tâches complexes en étapes plus petites et plus gérables.
        Il permet de suivre les progrès des sous-tâches et d'assurer une meilleure gestion des tâches.

    Note :
        Le champ 'employee_id' a été commenté dans le code.
        Si vous souhaitez assigner des employés aux sous-tâches, vous pouvez décommenter ce champ et l'utiliser.
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