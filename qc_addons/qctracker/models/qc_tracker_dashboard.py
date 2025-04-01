from odoo import models, fields, api

from odoo import models, fields, api

class QCTrackerDashboard(models.Model):
    _name = 'qctracker.dashboard'
    _description = 'QC Tracker Dashboard'

    employees_count = fields.Integer(string="Total Employees", compute='_compute_counts')
    projects_count = fields.Integer(string="Total Projects", compute='_compute_counts')
    tasks_count = fields.Integer(string="Total Tasks", compute='_compute_counts')
    subtasks_count = fields.Integer(string="Total Subtasks", compute='_compute_counts')

    progress = fields.Float(string="Overall Progress", compute='_compute_progress')
    ongoing_projects_count = fields.Integer(string="Ongoing Projects", compute='_compute_ongoing_projects')
    completed_tasks_count = fields.Integer(string="Completed Tasks", compute='_compute_completed_tasks')
    pending_tasks_count = fields.Integer(string="Pending Tasks", compute='_compute_pending_tasks')

    @api.depends_context('active_test')
    def _compute_counts(self):
        """Optimisation des requêtes pour récupérer les totaux."""
        counts = {
            model: self.env[model].search_count([])
            for model in ['qctracker.employee', 'qctracker.project', 'qctracker.task', 'qctracker.subtask']
        }
        for rec in self:
            rec.employees_count = counts['qctracker.employee']
            rec.projects_count = counts['qctracker.project']
            rec.tasks_count = counts['qctracker.task']
            rec.subtasks_count = counts['qctracker.subtask']

    @api.depends('subtasks_count')
    def _compute_progress(self):
        """Calcul de la progression globale."""
        completed_subtasks = self.env['qctracker.subtask'].search_count([('state', '=', 'done')])
        total_subtasks = self.env['qctracker.subtask'].search_count([])
        for rec in self:
            rec.progress = (completed_subtasks / total_subtasks) * 100 if total_subtasks else 0.0

    @api.depends('projects_count')
    def _compute_ongoing_projects(self):
        """Nombre de projets en cours."""
        for rec in self:
            rec.ongoing_projects_count = self.env['qctracker.project'].search_count([('state', '=', 'in_progress')])

    @api.depends('tasks_count')
    def _compute_completed_tasks(self):
        """Nombre de tâches terminées."""
        for rec in self:
            rec.completed_tasks_count = self.env['qctracker.task'].search_count([('state', '=', 'done')])

    @api.depends('tasks_count')
    def _compute_pending_tasks(self):
        """Nombre de tâches en attente."""
        for rec in self:
            rec.pending_tasks_count = self.env['qctracker.task'].search_count([('state', '=', 'pending')])
