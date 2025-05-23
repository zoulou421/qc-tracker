# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class QCTrackerProcessProjectProject(models.Model):
    _name = 'qctracker.process.project.project'
    _description = 'Flux de Travail de Projet de Processus'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    # _rec_name = 'deliverable_id'

    active = fields.Boolean(default=True)
    name = fields.Char(string='Nom', required=True, default='Nouveau Projet de Processus')
    department_id = fields.Many2one('hr.department', string='Département')
    domain_id = fields.Many2one('qctracker.domain.project', string='Domaine', required=True)
    process_id = fields.Many2one('qctracker.process.project', string='Processus', required=True)
    sub_process_id = fields.Many2one('qctracker.sub_process.project', string='Sous-processus', required=True)
    activity_id = fields.Many2one('qctracker.activity.project', string='Activité', required=True)
    procedure_id = fields.Many2one('qctracker.procedure.project', string='Procédure', required=True)
    deliverable_id = fields.Many2one('qctracker.deliverable.project', string='Livrable', required=True)
    task_formulation_id = fields.Many2one('qctracker.task_formulation.project', string='Formulation des Tâches',
                                          required=True)
    notes = fields.Text(string='Notes')
    employee_id = fields.Many2one('hr.employee', string='Responsable')

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
        return {'domain': {'sub_process_id': [('process_id', "=", self.process_id.id)]}}

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
        return {'domain': {
            'deliverable_id': [('procedure_id', '=', self.procedure_id.id)],
            'task_formulation_id': [('procedure_id', '=', self.procedure_id.id)]
        }}

    @api.constrains('domain_id', 'process_id', 'sub_process_id', 'activity_id', 'procedure_id', 'deliverable_id',
                    'task_formulation_id')
    def _check_hierarchy(self):
        for record in self:
            if record.process_id and record.process_id.domain_id != record.domain_id:
                raise ValidationError("Le processus sélectionné n'appartient pas au domaine sélectionné.")
            if record.sub_process_id and record.sub_process_id.process_id != record.process_id:
                raise ValidationError("Le sous-processus sélectionné n'appartient pas au processus sélectionné.")
            if record.activity_id and record.activity_id.sub_process_id != record.sub_process_id:
                raise ValidationError("L'activité sélectionnée n'appartient pas au sous-processus sélectionné.")
            if record.procedure_id and record.procedure_id.activity_id != record.activity_id:
                raise ValidationError("La procédure sélectionnée n'appartient pas à l'activité sélectionnée.")
            if record.deliverable_id and record.deliverable_id.procedure_id != record.procedure_id:
                raise ValidationError("Le livrable sélectionné n'appartient pas à la procédure sélectionnée.")
            if record.task_formulation_id and record.task_formulation_id.procedure_id != record.procedure_id:
                raise ValidationError(
                    "La formulation des tâches sélectionnée n'appartient pas à la procédure sélectionnée.")

    @api.model
    def _import_check_hierarchy(self, vals):
        """Crée automatiquement les enregistrements manquants lors de l'importation, respectant les titres des champs."""
        model_fields = {
            'department_id': ('hr.department', None),
            'domain_id': ('qctracker.domain.project', None),
            'process_id': ('qctracker.process.project', 'domain_id'),
            'sub_process_id': ('qctracker.sub_process.project', 'process_id'),
            'activity_id': ('qctracker.activity.project', 'sub_process_id'),
            'procedure_id': ('qctracker.procedure.project', 'activity_id'),
            'deliverable_id': ('qctracker.deliverable.project', 'procedure_id'),
            'task_formulation_id': ('qctracker.task_formulation.project', 'procedure_id'),
            'employee_id': ('hr.employee', None),
        }

        for field, (model_name, parent_field) in model_fields.items():
            if field in vals and vals[field]:
                # Skip if value is an ID (e.g., from import with ID mapping)
                if isinstance(vals[field], (int, float)):
                    continue
                # Try to find by name
                record = self.env[model_name].search([('name', '=', vals[field])], limit=1)
                if not record:
                    # Create new record
                    create_vals = {'name': vals[field]}
                    if parent_field and parent_field in vals:
                        # Find or create parent record
                        parent_record = self.env[model_name.rsplit('.', 1)[0]].search(
                            [('name', '=', vals[parent_field])], limit=1)
                        if not parent_record and parent_field in model_fields:
                            parent_model = model_fields[parent_field][0]
                            parent_record = self.env[parent_model].create({'name': vals[parent_field]})
                        create_vals[parent_field] = parent_record.id
                    record = self.env[model_name].create(create_vals)
                vals[field] = record.id

        if not vals.get('deliverable_id'):
            raise ValidationError("Le champ 'Livrable' (deliverable_id) est requis pour l'importation.")
        if not vals.get('name'):
            vals['name'] = 'Nouveau Projet de Processus'

        # Validate hierarchy
        self._check_hierarchy()
