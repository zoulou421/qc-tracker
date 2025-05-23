# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class QCTrackerProcessProjectProject(models.Model):
    _name = 'qctracker.process.project.project'
    _description = 'Process Project Workflow Project'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', required=True, default='New Process Project')

    department_id = fields.Many2one('hr.department', string='Department')

    domain_id = fields.Many2one('qctracker.domain.project', string='Domain', required=True)
    process_id = fields.Many2one('qctracker.process.project', string='Process', required=True)
    sub_process_id = fields.Many2one('qctracker.sub_process.project', string='Sub Process', required=True)
    activity_id = fields.Many2one('qctracker.activity.project', string='Activity', required=True)
    procedure_id = fields.Many2one('qctracker.procedure.project', string='Procedure', required=True)
    deliverable_id = fields.Many2one('qctracker.deliverable.project', string='Deliverable', required=True)
    task_formulation_id = fields.Many2one('qctracker.task_formulation.project', string='Task Formulation',
                                          required=True)
    notes = fields.Text(string='Notes')
    project_id = fields.Many2one('qctracker.project', string='Project', options="{'no_create_edit': True}")

    #employee_id = fields.Many2one('qctracker.employee', string='Assigned Employee', options="{'no_create_edit': True}")
    employee_id = fields.Many2one('hr.employee', string='Assigned Employee', options="{'no_create_edit': True}")

    @api.onchange('domain_id')
    def _onchange_domain_id(self):
        self.process_id = False
        self.sub_process_id = False
        self.activity_id = False
        self.procedure_id = False
        self.deliverable_id = False
        self.task_formulation_id = False
        return {'domain': {'process_id': [('domain_id', '=', self.domain_id.id)]}}

    @api.onchange('process_id')
    def _onchange_process_id(self):
        self.sub_process_id = False
        self.activity_id = False
        self.procedure_id = False
        self.deliverable_id = False
        self.task_formulation_id = False
        return {'domain': {'sub_process_id': [('process_id', '=', self.process_id.id)]}}

    @api.onchange('sub_process_id')
    def _onchange_sub_process_id(self):
        self.activity_id = False
        self.procedure_id = False
        self.deliverable_id = False
        self.task_formulation_id = False
        return {'domain': {'activity_id': [('sub_process_id', '=', self.sub_process_id.id)]}}

    @api.onchange('activity_id')
    def _onchange_activity_id(self):
        self.procedure_id = False
        self.deliverable_id = False
        self.task_formulation_id = False
        return {'domain': {'procedure_id': [('activity_id', '=', self.activity_id.id)]}}

    @api.onchange('procedure_id')
    def _onchange_procedure_id(self):
        self.deliverable_id = False
        self.task_formulation_id = False
        return {'domain': {'deliverable_id': [('procedure_id', '=', self.procedure_id.id)],
                           'task_formulation_id': [('procedure_id', '=', self.procedure_id.id)]}}

    @api.constrains('domain_id', 'process_id', 'sub_process_id', 'activity_id', 'procedure_id', 'deliverable_id',
                    'task_formulation_id')
    def _check_hierarchy(self):
        for record in self:
            if record.process_id and record.process_id.domain_id != record.domain_id:
                raise ValidationError("Selected process does not belong to the selected domain.")
            if record.sub_process_id and record.sub_process_id.process_id != record.process_id:
                raise ValidationError("Selected sub-process does not belong to the selected process.")
            if record.activity_id and record.activity_id.sub_process_id != record.sub_process_id:
                raise ValidationError("Selected activity does not belong to the selected sub-process.")
            if record.procedure_id and record.procedure_id.activity_id != record.activity_id:
                raise ValidationError("Selected procedure does not belong to the selected activity.")
            if record.deliverable_id and record.deliverable_id.procedure_id != record.procedure_id:
                raise ValidationError("Selected deliverable does not belong to the selected procedure.")
            if record.task_formulation_id and record.task_formulation_id.procedure_id != record.procedure_id:
                raise ValidationError("Selected task formulation does not belong to the selected procedure.")
