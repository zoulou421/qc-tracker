# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

"""
===========Objectif=========== :
Ce modèle représente une notification de tâche.
Il permet de gérer les notifications envoyées aux employés concernant les tâches.

==============Champs=============== :
task_id (Many2one vers qctracker.task) : La tâche associée à la notification.
recipient_id (Many2one vers qctracker.employee) : L'employé destinataire de la notification.
message (Text) : Le contenu du message de la notification.
notification_type (Selection) : Le type de notification (e-mail, interne, SMS).
is_sent (Boolean) : Indique si la notification a été envoyée.
is_read (Boolean) : Indique si la notification a été lue.
attachment_ids (Many2many vers ir.attachment) : Les pièces jointes de la notification.
scheduled_date (Datetime) : La date de planification de l'envoi de la notification.
template_id (Many2one vers mail.template) : Le modèle d'e-mail utilisé pour la notification.
date_created (Datetime) : La date de création de la notification.

==============Méthodes=========== :
send_email_notification() : Envoie une notification par e-mail au destinataire.

=============Fonctionnalités Clés=============== :
Gestion des notifications de tâches.
Gestion de différents types de notifications.
Suivi de l'état d'envoi et de lecture des notifications.
Gestion des pièces jointes et de la planification.
Utilisation de modèles d'e-mails.
gestion de la date de création.

=============Utilisation=============== :
Ce modèle est utilisé pour envoyer des notifications aux employés concernant les tâches.
Permet d'avoir une communication efficace au sein de l'application.
"""
class QCTrackerTaskNotification(models.Model):
    """
    Modèle Odoo représentant une notification de tâche.
    Ce modèle permet de gérer les notifications envoyées aux employés concernant les tâches.
    """
    _name = 'qctracker.task.notification'
    _description = 'Task Notification'

    task_id = fields.Many2one('qctracker.task', string='Task')
    recipient_id = fields.Many2one('qctracker.employee', string='Recipient')
    message = fields.Text(string='Message')
    notification_type = fields.Selection([
        ('email', 'Email'),
        ('internal', 'Internal'),
        ('sms', 'SMS')
    ], string='Notification Type', default='email')
    is_sent = fields.Boolean(string='Is Sent', default=False)
    is_read = fields.Boolean(string='Is Read', default=False)
    attachment_ids = fields.Many2many('ir.attachment', string='Attachments')
    scheduled_date = fields.Datetime(string='Scheduled Date')
    template_id = fields.Many2one('mail.template', string='Email Template')
    date_created = fields.Datetime(string='Date de Création', default=fields.Datetime.now)

    def send_email_notification(self):
        """
        Envoie une notification par e-mail au destinataire de la notification.
        Utilise un modèle d'e-mail défini dans Odoo.
        Marque la notification comme envoyée après l'envoi de l'e-mail.
        """
        for notification in self:
            try:
                if notification.template_id:
                    notification.template_id.send_mail(notification.id, force_send=True)
                else:
                    template = self.env.ref('qctracker.email_template_task_notification')
                    template.send_mail(notification.id, force_send=True)
                notification.is_sent = True
            except Exception as e:
                _logger.error(f"Failed to send email notification: {e}")
                raise UserError(f"Failed to send email notification: {e}")
