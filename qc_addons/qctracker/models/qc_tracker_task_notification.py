# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class QCTrackerTaskNotification(models.Model):
    _name = 'qctracker.task.notification'
    _description = 'Task Notification'
    _inherit = ['mail.thread']

    task_id = fields.Many2one('qctracker.task', string='Task')
    recipient_id = fields.Many2one('qctracker.employee', string='Recipient')
    message = fields.Text(string='Message')
    notification_type = fields.Selection([
        ('internal', 'Internal'),
        ('sms', 'SMS')
    ], string='Notification Type', default='internal')
    is_sent = fields.Boolean(string='Is Sent', default=False)
    is_read = fields.Boolean(string='Is Read', default=False)
    attachment_ids = fields.Many2many('ir.attachment', string='Attachments')
    scheduled_date = fields.Datetime(string='Scheduled Date')
    date_created = fields.Datetime(string='Date de Création', default=fields.Datetime.now)

    def send_internal_notification(self):
        """
        Envoie une notification interne au destinataire via la boîte de réception Odoo.
        Poste un message dans la boîte de réception de l'utilisateur associé.
        Marque la notification comme envoyée.
        """
        for notification in self:
            if not notification.recipient_id.user_id:
                _logger.error(f"No user associated with employee {notification.recipient_id.name}")
                raise UserError(f"No user associated with employee {notification.recipient_id.name}")
            try:
                # Poster un message dans la boîte de réception de l'utilisateur
                self.env['mail.message'].create({
                    'model': 'qctracker.task.notification',
                    'res_id': notification.id,
                    'message_type': 'notification',
                    'subtype_id': self.env.ref('mail.mt_note').id,
                    'body': f"<p>{notification.message}</p><p>Task: <a href='/web#id={notification.task_id.id}&model=qctracker.task&view_type=form'>{notification.task_id.name}</a></p>",
                    'partner_ids': [(4, notification.recipient_id.user_id.partner_id.id)],
                })
                notification.is_sent = True
                # Poster dans le chatter de la notification
                notification.message_post(
                    body=f"Internal notification sent to {notification.recipient_id.name}",
                    message_type='notification',
                    subtype_id=self.env.ref('mail.mt_comment').id
                )
            except Exception as e:
                _logger.error(f"Failed to send internal notification: {e}")
                raise UserError(f"Failed to send internal notification: {e}")

    def action_mark_as_read(self):
        """Marque la notification comme lue."""
        self.ensure_one()
        self.is_read = True
        self.message_post(
            body="Notification marked as read",
            message_type='notification',
            subtype_id=self.env.ref('mail.mt_comment').id
        )
