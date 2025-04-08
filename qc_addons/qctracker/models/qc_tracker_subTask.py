# -*- coding: utf-8 -*-

from odoo import models, fields, api

class QCTrackerSubTask(models.Model):
    """
    Modèle Odoo représentant une sous-tâche.

    Objectif :
        Ce modèle représente une sous-tâche, une étape plus petite et détaillée d'une tâche principale.
        Il permet de décomposer les tâches complexes en sous-tâches plus gérables, facilitant ainsi la planification,
        l'exécution et le suivi des projets.

    Champs :
        task_id (Many2one vers qctracker.task) :
            La tâche principale à laquelle la sous-tâche appartient.
            Ce champ établit une relation Many2one avec le modèle 'qctracker.task', permettant d'associer chaque sous-tâche à une tâche principale spécifique.
            Il est essentiel pour maintenir la structure hiérarchique des tâches et sous-tâches.

        name (Char, obligatoire) :
            Le nom de la sous-tâche.
            Ce champ est obligatoire et stocke le nom de la sous-tâche, servant d'identifiant unique et clair.

        description (Text) :
            La description détaillée de la sous-tâche.
            Ce champ stocke une description textuelle détaillée de la sous-tâche, fournissant des informations supplémentaires sur ce qu'elle implique,
            les étapes à suivre, les ressources nécessaires, etc.

        start_date (Date) :
            La date de début de la sous-tâche.
            Ce champ stocke la date à laquelle la sous-tâche doit commencer, permettant de planifier le calendrier du projet.

        end_date (Date) :
            La date de fin de la sous-tâche.
            Ce champ stocke la date à laquelle la sous-tâche doit être terminée, permettant de suivre les échéances et d'assurer le respect des délais.

        status (Selection) :
            Le statut de la sous-tâche.
            Ce champ stocke le statut actuel de la sous-tâche, permettant de suivre sa progression.
            Les options de statut sont 'in_progress' (En cours) et 'completed' (Terminé).
            Il facilite la communication et la coordination entre les membres de l'équipe.

        employee_id (Many2one vers qctracker.employee, optionnel) :
            L'employé assigné à la sous-tâche.
            Ce champ établit une relation Many2one avec le modèle 'qctracker.employee', permettant d'assigner une sous-tâche à un employé spécifique.
            Il est commenté par défaut, mais peut être décommenté pour activer l'assignation d'employés aux sous-tâches.

    Fonctionnalités Clés :
        - Gestion des sous-tâches : Permet de créer, modifier et supprimer des sous-tâches.
        - Association des sous-tâches aux tâches principales : Établit une relation claire entre les sous-tâches et leurs tâches principales.
        - Suivi des dates de début et de fin des sous-tâches : Permet de planifier et de suivre les échéances des sous-tâches.
        - Suivi du statut des sous-tâches : Permet de suivre la progression des sous-tâches et de s'assurer qu'elles sont terminées à temps.
        - Assignation des employés aux sous-tâches (optionnel) : Permet d'assigner des employés spécifiques aux sous-tâches.

    Utilisation :
        Ce modèle est utilisé pour décomposer les tâches complexes en étapes plus petites et plus gérables.
        Il permet de suivre les progrès des sous-tâches, d'assurer une meilleure gestion des tâches, et de faciliter la collaboration et la communication entre les membres de l'équipe.

    Note :
        Le champ 'employee_id' a été commenté dans le code.
        Si vous souhaitez assigner des employés aux sous-tâches, vous pouvez décommenter ce champ et l'utiliser.
    """
    _name = 'qctracker.subtask'
    _description = 'A Sub_Task depends on a Task'

    task_id = fields.Many2one('qctracker.task', string='Task')
    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    employee_id = fields.Many2one('qctracker.employee', string='Assigned Employee') # Décommenter pour activer l'assignation d'employés
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    status = fields.Selection([('in_progress', 'In Progress'), ('completed', 'Completed')], string='Status')