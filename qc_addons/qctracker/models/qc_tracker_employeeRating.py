# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

"""

========Objectif====== :
Ce modèle représente une évaluation d'employé effectuée par un manager pour un projet donné.
Il permet de suivre les performances des employés et de fournir des commentaires structurés.


========Champs====== :
employee_id (Many2one vers qctracker.employee) : L'employé évalué.
project_id (Many2one vers qctracker.project) : Le projet sur lequel l'évaluation est basée.
rating (Integer, par défaut 0) : La note de l'employé (de 0 à 10).
on_time (Boolean) : Indique si l'employé a respecté les délais.
comments (Text) : Les commentaires du manager.
evaluation_date (Date) : La date de l'évaluation.
state (Selection, par défaut 'draft') : Le statut de l'évaluation (draft, submitted).
manager_id (Many2one vers res.users, par défaut l'utilisateur courant) : Le manager qui a effectué l'évaluation.


=======Méthodes======== :
_check_rating_range() : Valide que la note est comprise entre 0 et 10.
_check_submitted_modification() : Empêche la modification des évaluations soumises.
action_submit() : Soumet l'évaluation.
action_reset() : Réinitialise l'évaluation à l'état brouillon.
get_rating_label() : Retourne une étiquette textuelle pour la note.
_compute_employee_average_rating() : Calcule la note moyenne d'un employé.

=======Fonctionnalités Clés========= :
Gestion des évaluations des employés par projet.
Validation des notes et des modifications.
Suivi des délais et des commentaires.
Gestion des statuts des évaluations.
Calcul de note moyenne de l'employé.

=========Utilisation========= :
Ce modèle est essentiel pour évaluer les performances des employés et fournir un feedback structuré.
Il permet de suivre les progrès des employés et d'identifier les domaines d'amélioration.

"""

# --- QCTrackerEmployeeRating Model ---
class QCTrackerEmployeeRating(models.Model):
    """
    Modèle Odoo représentant une évaluation d'employé.
    Une évaluation est donnée par un manager pour évaluer un employé sur un projet.
    """
    _name = 'qctracker.employeerating'
    _description = 'An Employee_Rating is given by a Manager to evaluate an Employee'

    employee_id = fields.Many2one('qctracker.employee', string='Employee')
    # project_id = fields.Many2one('qctracker.project', string='Project')
    rating = fields.Integer(string='Rating', default=0, help='Evaluation from 0 to 10')
    on_time = fields.Boolean(string='On Time')
    comments = fields.Text(string='Comments')
    evaluation_date = fields.Date(string='Evaluation Date')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
    ], string='Status', default='draft')
    manager_id = fields.Many2one('res.users', string='Manager', default=lambda self: self.env.user)

    @api.constrains('rating')
    def _check_rating_range(self):
        """
        Valide que la note est comprise entre 0 et 10.
        """
        for record in self:
            if record.rating < 0 or record.rating > 10:
                raise ValidationError("Rating must be between 0 and 10.")

    @api.constrains('state')
    def _check_submitted_modification(self):
        """
        Empêche la modification des évaluations soumises.
        """
        for record in self:
            if record.state == 'submitted' and (record.rating != record._origin.rating or
                                               record.on_time != record._origin.on_time or
                                               record.comments != record._origin.comments or
                                               record.evaluation_date != record._origin.evaluation_date):
                raise ValidationError("You cannot modify a submitted rating.")

    @api.model
    def action_submit(self):
        """
        Soumet l'évaluation de l'employé en changeant l'état à 'submitted'.
        """
        for record in self:
            if not record.rating:
                raise ValidationError("Please provide a rating before submitting.")
            if not record.evaluation_date:
                raise ValidationError("Please provide an evaluation date before submitting.")
            record.state = 'submitted'
        return True

    @api.model
    def action_reset(self):
        """
        Réinitialise les champs de l'évaluation à leur état initial et change l'état à 'draft'.
        """
        for record in self:
            record.rating = 0
            record.on_time = False
            record.comments = False
            record.evaluation_date = False
            record.state = 'draft'
        return True

    def get_rating_label(self):
        """
        Retourne l'étiquette textuelle de la note en fonction de la valeur de la note.
        """
        self.ensure_one()
        labels = {
            0: 'Very Bad',
            1: 'Bad',
            2: 'Mediocre',
            3: 'Insufficient',
            4: 'Passable',
            5: 'Average',
            6: 'Acceptable',
            7: 'Good',
            8: 'Very Good',
            9: 'Excellent',
            10: 'Perfect',
        }
        return labels.get(self.rating, '')

    @api.model
    def _compute_employee_average_rating(self, employee_id):
        """
        Calcule la note moyenne d'un employé en fonction de ses évaluations soumises.
        """
        ratings = self.search([('employee_id', '=', employee_id), ('state', '=', 'submitted')])
        if ratings:
            total_rating = sum(rating.rating for rating in ratings)
            return total_rating / len(ratings)
        return 0
