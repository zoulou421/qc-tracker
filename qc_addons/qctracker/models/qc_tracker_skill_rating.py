# -*- coding: utf-8 -*-

from odoo import models, fields, api

"""
============Objectif========== :
Ce modèle représente une évaluation détaillée des compétences d'un employé dans le cadre d'une évaluation globale.
Il permet de noter chaque compétence individuellement avec un niveau de compétence spécifique et des commentaires.

===========Champs============ :
rating_id (Many2one vers qctracker.employeerating, obligatoire, suppression en cascade) : L'évaluation globale de l'employé à laquelle cette évaluation de compétence est liée.
skill_id (Many2one vers qctracker.skill, obligatoire) : La compétence évaluée.
rating (Selection, obligatoire) : Le niveau de compétence (Basique, Intermédiaire, Avancé, Expert).
comments (Text) : Les commentaires ou les notes concernant l'évaluation de la compétence.

=============Fonctionnalités Clés============== :
Gestion des évaluations détaillées des compétences.
Association des évaluations de compétences aux évaluations d'employés et aux compétences.
Suivi des niveaux de compétence et des commentaires.
Assure que chaque évaluation de compétence est liée à une évaluation d'employé et à une compétence.

=================Utilisation============= :
Ce modèle est utilisé pour fournir une évaluation détaillée des compétences des employés.
Permet d'avoir une vision précise des compétences des employés.
"""
class QCTrackerSkillRating(models.Model):
    """
    Modèle Odoo représentant une évaluation détaillée des compétences dans le cadre d'une évaluation d'employé.
    Ce modèle permet de noter individuellement chaque compétence d'un employé lors d'une évaluation.
    """
    _name = 'qctracker.skillrating'
    _description = 'Skill Rating in Evaluation'

    rating_id = fields.Many2one(
        'qctracker.employeerating',
        string='Evaluation',
        required=True,
        ondelete='cascade'
    )
    skill_id = fields.Many2one('qctracker.skill', string='Skill', required=True)
    rating = fields.Selection([
        ('1', 'Basic'),
        ('2', 'Intermediate'),
        ('3', 'Advanced'),
        ('4', 'Expert')
    ], string='Rating', required=True)
    comments = fields.Text(string='Comments')