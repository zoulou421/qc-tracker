# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re

"""
=====Objectif===== :
Ce modèle représente un employé au sein de votre application Odoo.
Il permet de gérer les informations relatives aux employés, tels que leur nom, leurs coordonnées, leur rôle, leur département, leurs compétences, leurs tâches, leurs évaluations, etc.

====Champs==== :
name (Char, calculé et stocké) : Le nom complet de l'employé.
first_name (Char, obligatoire) : Le prénom de l'employé.
last_name (Char, obligatoire) : Le nom de famille de l'employé.
email (Char, obligatoire et unique) : L'adresse e-mail de l'employé.
phone (Char) : Le numéro de téléphone de l'employé.
role (Selection, obligatoire) : Le rôle de l'employé (employé, manager, admin).
department_id (Many2one vers qctracker.department) : Le département auquel l'employé appartient.
is_manager (Boolean, calculé et stocké) : Indique si l'employé est un manager.
skill_ids (Many2many vers qctracker.skill) : Les compétences de l'employé.
task_ids (One2many vers qctracker.task) : Les tâches assignées à l'employé.
rating_employee_ids (One2many vers qctracker.employeerating) : Les évaluations de l'employé.
gender (Selection) : Le genre de l'employé.
country_id (Many2one vers res.country) : Le pays de l'employé.
project_ids (One2many vers qctracker.project) : Les projets auxquels l'employé est associé.
user_id (Many2one vers res.users) : L'utilisateur Odoo associé à l'employé.
notification_ids (One2many vers qctracker.task.notification) : Les notifications associées à l'employé.
country_dynamic (Selection) : Une liste dynamique des pays.

======Méthodes===== :
_compute_full_name() : Calcule le nom complet de l'employé.
_compute_is_manager() : Détermine si l'employé est un manager.
_get_country_selection() : Récupère la liste des pays pour la sélection dynamique.
_check_email() : Valide l'adresse e-mail de l'employé.
_check_phone() : Valide le numéro de téléphone de l'employé.

=====Fonctionnalités Clés====== :
Gestion des informations de base des employés.
Association des employés aux départements, projets et tâches.
Gestion des compétences et des évaluations des employés.
Validation des coordonnées des employés.
Gestion des notifications.

======Utilisation====== :
Ce modèle est essentiel pour gérer les employés au sein de votre application Odoo.
Il permet de centraliser les informations relatives aux employés et de faciliter la gestion des ressources humaines.
"""


# --- QCTrackerEmployee Model ---
class QCTrackerEmployee(models.Model):
    """
    Modèle Odoo représentant un employé.
    Un employé peut appartenir à un département, être un manager, et avoir des compétences.
    """
    _name = 'qctracker.employee'
    _description = 'An Employee can belong to a Department and be a Manager'

    name = fields.Char(string='Full Name', compute='_compute_full_name', store=True)
    first_name = fields.Char(string='First Name', required=True, size=256)
    last_name = fields.Char(string='Last Name', required=True, size=256)
    email = fields.Char(string='Email', required=True, unique=True, widget="email")
    phone = fields.Char(string='Phone', size=32, widget="phone")
    role = fields.Selection([
        ('employee', 'Employee'),
        ('manager', 'Manager'),
        ('admin', 'Admin')
    ], string='Role', required=True)
    department_id = fields.Many2one('qctracker.department', string='Department')
    is_manager = fields.Boolean(string='Is Manager', compute='_compute_is_manager', store=True)
    # skill_ids = fields.Many2many('qctracker.skill', string='Skills')  # Gestion des compétences

    task_ids = fields.One2many('qctracker.task', 'employee_id', string='Assigned Tasks')
    rating_employee_ids = fields.One2many('qctracker.employeerating', 'employee_id', 'Ratings')
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string='Gender')
    country_id = fields.Many2one('res.country', string='Pays (ID)')
    project_ids = fields.One2many('qctracker.project', 'employee_id', string='Projects')
    user_id = fields.Many2one('res.users', string='Associated User')
    project_delivery_ids = fields.One2many('qctracker.projectdelivery','employee_id', string='Project Delivery')

    notification_ids = fields.One2many('qctracker.task.notification', 'recipient_id', string='Notifications')

    country_dynamic = fields.Selection(
        '_get_country_selection', string='Pays (Dynamique)',
        help='Select a country (dynamic list)')

    @api.depends('first_name', 'last_name')
    def _compute_full_name(self):
        """
        Calcule le nom complet de l'employé en combinant le prénom et le nom de famille.
        """
        for rec in self:
            rec.name = f"{rec.first_name} {rec.last_name}" if rec.first_name and rec.last_name else ''

    @api.depends('role')
    def _compute_is_manager(self):
        """
        Détermine si l'employé est un manager en fonction de son rôle.
        """
        for rec in self:
            rec.is_manager = rec.role == 'manager'

    @api.model
    def _get_country_selection(self):
        """
        Récupère la liste des pays disponibles pour la sélection dynamique.
        """
        countries = self.env['res.country'].search([])
        return [(str(country.id), country.name) for country in sorted(countries, key=lambda country: country.name)]

    @api.constrains('email')
    def _check_email(self):
        """
        Valide l'adresse e-mail de l'employé en utilisant une expression régulière.
        """
        for record in self:
            if record.email and not re.match(r"[^@]+@[^@]+\.[^@]+", record.email):
                raise ValidationError("Invalid email address.")

    @api.constrains('phone')
    def _check_phone(self):
        """
        Valide le numéro de téléphone de l'employé.
        """
        for record in self:
            if record.phone and not record.phone.isdigit():
                raise ValidationError("Invalid phone number. Only digits are allowed.")
