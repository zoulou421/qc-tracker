from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class QCTrackerDepartment(models.Model):
    _name = 'qctracker.department'
    _description = 'A Department has several Employees'

    name = fields.Char(string='Name', required=True)
    manager_id = fields.Many2one('qctracker.employee', string='Manager')
    employee_count = fields.Integer(string='Employee Count', compute='_compute_employee_count', store=True)
    active = fields.Boolean(string='Active', default=True)

    @api.depends('manager_id')
    def _compute_employee_count(self):
        """Compute the number of employees in the department."""
        for department in self:
            department.employee_count = self.env['qctracker.employee'].search_count([('department_id', '=', department.id)])

    def action_activate(self):
        """Activate the department."""
        self.write({'active': True})

    def action_deactivate(self):
        """Deactivate the department."""
        self.write({'active': False})
