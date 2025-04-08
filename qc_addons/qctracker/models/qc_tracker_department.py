# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

"""
======Objectif====== :
Ce modèle représente un département au sein de votre application Odoo.
Il permet de gérer les informations relatives aux départements, tels que leur nom, leur manager, et les employés et projets associés.

======Champs===== :
name (Char, obligatoire) : Le nom du département.
manager_id (Many2one vers qctracker.employee) : Le manager responsable du département.
employee_count (Integer, calculé et stocké) : Le nombre d'employés appartenant au département.
active (Boolean, par défaut True) : Indique si le département est actif.
project_ids (One2many vers qctracker.project) : Les projets associés au département.

======Méthodes====== :
_compute_employee_count() : Calcule et stocke le nombre d'employés dans le département.
action_activate() : Active le département.
action_deactivate() : Désactive le département.

=======Fonctionnalités Clés====== :
Gestion des informations de base des départements.
Association des employés et des projets aux départements.
Suivi du nombre d'employés par département.
Gestion de l'état actif/inactif des départements.

======Utilisation====== :
Ce modèle est essentiel pour organiser les employés et les projets au sein de votre application.
Il permet de structurer les données et de faciliter la gestion des ressources.
"""

# --- QCTrackerDepartment Model ---
class QCTrackerDepartment(models.Model):
    """
    Modèle Odoo représentant un département.
    Un département peut avoir plusieurs employés et projets associés.
    """
    _name = 'qctracker.department'
    _description = 'A Department has several Employees'

    name = fields.Char(string='Name', required=True)
    employee_ids = fields.One2many('qctracker.employee', 'department_id', string='Employees')
    employee_count = fields.Integer(string='Employee Count', compute='_compute_employee_count', store=True)
    active = fields.Boolean(string='Active', default=True)
    project_ids = fields.One2many('qctracker.project', 'department_id', string='Projects')

    @api.depends('employee_ids')
    def _compute_employee_count(self):
        """
        Calcule le nombre d'employés associés au département.
        Ce champ est calculé et stocké pour améliorer les performances.
        """
        for department in self:
            department.employee_count = self.env['qctracker.employee'].search_count(
                [('department_id', '=', department.id)])

    def action_activate(self):
        """
        Active le département en définissant le champ 'active' sur True.
        """
        self.write({'active': True})

    def action_deactivate(self):
        """
        Désactive le département en définissant le champ 'active' sur False.
        """
        self.write({'active': False})