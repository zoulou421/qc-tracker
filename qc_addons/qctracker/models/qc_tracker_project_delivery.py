# -*- coding: utf-8 -*-

from odoo import models, fields, api

"""
========Objectif======= :
Ce modèle représente la validation de la livraison d'un projet.
Il permet d'enregistrer la confirmation par un manager de la complétion et de la conformité d'un projet.

=======Champs======== :
project_id (Many2one vers qctracker.project) : Le projet concerné par la livraison.
manager_id (Many2one vers qctracker.employee) : Le manager qui a validé la livraison.
on_time (Boolean) : Indique si la livraison a été effectuée à temps.
comments (Text) : Les commentaires ou les notes du manager concernant la livraison.
delivery_date (Date) : La date de livraison validée.

==========Fonctionnalités Clés======== :
Gestion de la validation des livraisons de projets.
Enregistrement des informations de livraison, y compris la conformité et les commentaires.
Suivi des dates de livraison.

============Utilisation============ :
Ce modèle est essentiel pour assurer le suivi et la validation des livraisons de projets.
Il permet de garantir que les projets sont livrés conformément aux exigences et dans les délais impartis.
"""
class QCTrackerProjectDelivery(models.Model):
    """
    Modèle Odoo représentant la validation de la livraison d'un projet.
    Une livraison de projet est validée par un manager pour confirmer la complétion et la conformité.
    """
    _name = 'qctracker.projectdelivery'
    _description = 'A Project_Delivery is validated by a Manager'

    project_id = fields.Many2one('qctracker.project', string='Project')
    employee_id = fields.Many2one('qctracker.employee', string='Project Manager')
    on_time = fields.Boolean(string='On Time')
    comments = fields.Text(string='Comments')
    delivery_date = fields.Date(string='Delivery Date')