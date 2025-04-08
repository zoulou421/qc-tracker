# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class QCTrackerSkillCategory(models.Model):
    """
    Modèle Odoo représentant les catégories de compétences.

    Objectif :
        Ce modèle permet de regrouper les compétences des employés en différentes catégories,
        facilitant ainsi l'organisation et la gestion des compétences au sein de l'entreprise.

    Champs :
        name (Char, obligatoire et unique) :
            Le nom de la catégorie de compétences.
            Ce champ est obligatoire et doit être unique pour assurer l'unicité des catégories.

    Fonctionnalités Clés :
        - Gestion des catégories de compétences : Permet de créer, modifier et supprimer des catégories de compétences.
        - Unicité des noms de catégories : Assure qu'il n'y a pas de doublons de noms de catégories.

    Utilisation :
        Ce modèle est utilisé pour organiser et classer les compétences des employés,
        permettant ainsi une meilleure gestion des ressources humaines et une planification efficace des compétences.
    """
    _name = 'qctracker.skill.category'
    _description = 'Skill Category'

    name = fields.Char(string='Category Name', required=True, unique=True)


class QCTrackerSkill(models.Model):
    """
    Modèle Odoo représentant les compétences des employés.

    Objectif :
        Ce modèle permet de gérer les compétences que les employés possèdent,
        y compris leur niveau, leur catégorie, leur dernière utilisation et leur statut.

    Champs :
        name (Char, obligatoire et unique) :
            Le nom de la compétence.
            Ce champ est obligatoire et doit être unique pour assurer l'unicité des compétences.

        description (Text) :
            La description de la compétence.
            Ce champ fournit des informations supplémentaires sur la compétence.

        category_id (Many2one vers qctracker.skill.category) :
            La catégorie de la compétence.
            Ce champ établit une relation Many2one avec le modèle 'qctracker.skill.category',
            permettant d'associer chaque compétence à une catégorie spécifique.

        level (Selection) :
            Le niveau de la compétence (débutant, intermédiaire, avancé).
            Ce champ permet de suivre le niveau de compétence de l'employé.

        last_used (Date) :
            La date de la dernière utilisation de la compétence.
            Ce champ permet de suivre la fréquence d'utilisation de la compétence.

        active (Boolean, par défaut True) :
            Indique si la compétence est active.
            Ce champ permet de désactiver les compétences obsolètes.

        employee_ids (Many2many vers qctracker.employee) :
            Les employés qui possèdent cette compétence.
            Ce champ établit une relation Many2many avec le modèle 'qctracker.employee',
            permettant d'associer plusieurs employés à une compétence.

    Méthodes :
        _check_unique_name() :
            Valide que le nom de la compétence est unique.
            Lève une exception ValidationError si le nom de la compétence existe déjà.

    Fonctionnalités Clés :
        - Gestion des compétences des employés : Permet de créer, modifier et supprimer des compétences.
        - Association des compétences aux catégories et aux employés : Permet de regrouper et d'attribuer des compétences.
        - Suivi du niveau et de la dernière utilisation des compétences : Permet d'évaluer et de planifier les compétences.
        - Unicité des noms de compétences : Assure qu'il n'y a pas de doublons de noms de compétences.

    Utilisation :
        Ce modèle est utilisé pour gérer les compétences des employés,
        faciliter la gestion des ressources humaines et optimiser l'allocation des compétences au sein de l'entreprise.
    """
    _name = 'qctracker.skill'
    _description = 'Employee Skill'

    name = fields.Char(string='Skill Name', required=True, unique=True)
    description = fields.Text(string='Description')
    category_id = fields.Many2one('qctracker.skill.category', string="Category")
    level = fields.Selection([
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced')
    ], string='Level')
    last_used = fields.Date(string='Last Used')
    active = fields.Boolean(string='Active', default=True)
    employee_ids = fields.Many2many('qctracker.employee', string="Employees")

    @api.constrains('name')
    def _check_unique_name(self):
        """
        Vérifie si le nom de la compétence est unique.
        Lève une exception ValidationError si le nom de la compétence existe déjà.
        """
        skills = self.search([('name', '=', self.name), ('id', '!=', self.id)])
        if skills:
            raise ValidationError("Skill name must be unique.")