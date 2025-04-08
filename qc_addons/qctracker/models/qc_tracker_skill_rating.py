# -*- coding: utf-8 -*-

from odoo import models, fields, api

class QCTrackerSkillRating(models.Model):
    """
    Modèle Odoo représentant une évaluation détaillée des compétences dans le cadre d'une évaluation d'employé.

    Objectif :
        Ce modèle permet de noter individuellement chaque compétence d'un employé lors d'une évaluation globale.
        Il permet de suivre et d'évaluer les compétences spécifiques de chaque employé avec des niveaux de compétence et des commentaires détaillés.

    Champs :
        rating_id (Many2one vers qctracker.employeerating, obligatoire, suppression en cascade) :
            L'évaluation globale de l'employé à laquelle cette évaluation de compétence est liée.
            Ce champ établit une relation Many2one avec le modèle 'qctracker.employeerating',
            assurant que chaque évaluation de compétence est associée à une évaluation d'employé.
            La suppression en cascade garantit que si l'évaluation d'employé est supprimée, les évaluations de compétence associées le sont également.

        skill_id (Many2one vers qctracker.skill, obligatoire) :
            La compétence évaluée.
            Ce champ établit une relation Many2one avec le modèle 'qctracker.skill',
            permettant d'associer chaque évaluation de compétence à une compétence spécifique.

        rating (Selection, obligatoire) :
            Le niveau de compétence (Basique, Intermédiaire, Avancé, Expert).
            Ce champ permet de noter le niveau de compétence de l'employé pour la compétence évaluée.

        comments (Text) :
            Les commentaires ou les notes concernant l'évaluation de la compétence.
            Ce champ permet d'ajouter des commentaires ou des notes détaillées sur l'évaluation de la compétence.

    Fonctionnalités Clés :
        - Gestion des évaluations détaillées des compétences : Permet de créer, modifier et supprimer des évaluations de compétences individuelles.
        - Association des évaluations de compétences aux évaluations d'employés et aux compétences : Assure une liaison claire entre les évaluations, les employés et les compétences.
        - Suivi des niveaux de compétence et des commentaires : Permet de documenter les niveaux de compétence et de fournir des commentaires détaillés.
        - Intégrité des données : Assure que chaque évaluation de compétence est liée à une évaluation d'employé et à une compétence.

    Utilisation :
        Ce modèle est utilisé pour fournir une évaluation détaillée des compétences des employés dans le cadre d'une évaluation globale.
        Il permet d'avoir une vision précise des compétences de chaque employé et de suivre leur évolution au fil du temps.
        Il est essentiel pour la gestion des performances, la planification des formations et le développement professionnel des employés.
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