# -*- coding: utf-8 -*-
from odoo import models, fields, api


class QCTrackerTaskNotification(models.Model):
    _name = 'qctracker.task.notification'
    _description = 'Task Notification'

    task_id = fields.Many2one('qctracker.task', string='Task')
    recipient_id = fields.Many2one('qctracker.employee', string='Recipient')
    message = fields.Text(string='Message')
    is_sent = fields.Boolean(string='Is Sent', default=False)

    def send_email_notification(self):
        for notification in self:
            template = self.env.ref('qctracker.email_template_task_notification')
            template.send_mail(notification.id, force_send=True)
            notification.is_sent = True