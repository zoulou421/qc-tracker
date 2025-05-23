# -*- coding: utf-8 -*-

from odoo import models, fields, api


class QCTrackerProjectDelivery(models.Model):
    """
    Modèle Odoo représentant la validation de la livraison d'un projet.

    Objectif :
        Ce modèle permet d'enregistrer et de gérer la validation de la livraison d'un projet par un manager.
        Il assure le suivi de la complétion, de la conformité et du respect des délais de livraison.

    Champs :
        project_id (Many2one vers qctracker.project) :
            Le projet concerné par la livraison.
            Ce champ établit une relation Many2one avec le modèle 'qctracker.project', permettant d'associer chaque livraison à un projet spécifique.

        employee_id (Many2one vers qctracker.employee) :
            Le manager qui a validé la livraison.
            Ce champ établit une relation Many2one avec le modèle 'qctracker.employee', enregistrant l'identité du manager responsable de la validation.

        on_time (Boolean) :
            Indique si la livraison a été effectuée à temps.
            Ce champ booléen permet de suivre le respect des délais de livraison.

        comments (Text) :
            Les commentaires ou les notes du manager concernant la livraison.
            Ce champ stocke les observations, les remarques ou les recommandations du manager concernant la livraison.

        delivery_date (Date) :
            La date de livraison validée.
            Ce champ enregistre la date à laquelle la livraison a été validée par le manager.

    Fonctionnalités Clés :
        - Gestion de la validation des livraisons de projets : Permet d'enregistrer et de suivre les validations de livraison.
        - Enregistrement des informations de livraison : Capture des détails essentiels tels que le projet, le manager, le respect des délais, les commentaires et la date de livraison.
        - Suivi des dates de livraison : Permet de surveiller et d'analyser les performances de livraison au fil du temps.
        - Assurance de la conformité : Facilite la vérification que les projets sont livrés conformément aux exigences.
        - Amélioration de la communication : Centralise les commentaires et les informations de livraison pour une meilleure communication entre les équipes.

    Utilisation :
        Ce modèle est essentiel pour assurer le suivi et la validation des livraisons de projets.
        Il permet de garantir que les projets sont livrés conformément aux exigences et dans les délais impartis.
        Il facilite également l'analyse des performances de livraison et l'identification des domaines d'amélioration.

    Note :
        Ce modèle est conçu pour être utilisé par les managers pour valider les livraisons de projets.
        Il est important de s'assurer que les informations saisies sont exactes et complètes pour une gestion efficace des livraisons.
    """
    _name = 'qctracker.projectdelivery'
    _description = 'A Project_Delivery is validated by a Manager'

    project_id = fields.Many2one('qctracker.project', string='Project')
    employee_id = fields.Many2one('qctracker.employee', string='Project Manager')
    on_time = fields.Boolean(string='On Time')
    comments = fields.Text(string='Comments')
    delivery_date = fields.Date(string='Delivery Date')
