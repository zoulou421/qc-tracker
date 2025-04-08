# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

"""
===========Objectif============ :
Ce modèle représente les catégories de compétences.
Il permet de regrouper les compétences des employés en différentes catégories (par exemple, technique, soft skills, langues).

===========Champs=========== :
name (Char, obligatoire et unique) : Le nom de la catégorie de compétences.

===========Fonctionnalités Clés============= :
Gestion des catégories de compétences.
Assure l'unicité des noms de catégories.

===============Utilisation================ :
Ce modèle est utilisé pour organiser et classer les compétences des employés.
Résumé du Modèle QCTrackerSkill :

===============Objectif============= :
Ce modèle représente les compétences que les employés peuvent posséder.
Il permet de gérer les compétences des employés, y compris leur niveau et leur catégorie.

=================Champs================= :
name (Char, obligatoire et unique) : Le nom de la compétence.
description (Text) : La description de la compétence.
category_id (Many2one vers qctracker.skill.category) : La catégorie de la compétence.
level (Selection) : Le niveau de la compétence (débutant, intermédiaire, avancé).
last_used (Date) : La date de la dernière utilisation de la compétence.
active (Boolean, par défaut True) : Indique si la compétence est active.
employee_ids (Many2many vers qctracker.employee) : Les employés qui possèdent cette compétence.

=================Méthodes================ :
_check_unique_name() : Valide que le nom de la compétence est unique.

============Fonctionnalités Clés================= :
Gestion des compétences des employés.
Association des compétences aux catégories et aux employés.
Suivi du niveau et de la dernière utilisation des compétences.
Assure l'unicité des noms de compétences.

================Utilisation================= :
Ce modèle est utilisé pour gérer les compétences des employés et faciliter la gestion des ressources humaines.
"""
class QCTrackerSkillCategory(models.Model):
    """
    Modèle Odoo représentant les catégories de compétences.
    Ce modèle permet de regrouper les compétences en différentes catégories.
    """
    _name = 'qctracker.skill.category'
    _description = 'Skill Category'

    name = fields.Char(string='Category Name', required=True, unique=True)


class QCTrackerSkill(models.Model):
    """
    Modèle Odoo représentant les compétences que les employés peuvent posséder.
    Ce modèle permet de gérer les compétences des employés, y compris leur niveau et leur catégorie.
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
