# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class QCTrackerProcessProjectProject(models.Model):
    _name = 'qctracker.process.project.project'
    _description = 'Flux de Travail de Projet de Processus'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'  # Ajout explicite de _rec_name

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
        """Import ultra-tolérant qui crée tout ce qui manque"""
        try:
            # 1. Gestion du département (non lié à la hiérarchie)
            if 'department_id' in vals and vals['department_id']:
                if isinstance(vals['department_id'], (int, float)):
                    if not self.env['hr.department'].browse(int(vals['department_id'])).exists():
                        vals['department_id'] = False
                else:
                    dept_name = str(vals['department_id']).strip()
                    if dept_name:
                        department = self.env['hr.department'].search([('name', '=ilike', dept_name)], limit=1)
                        if not department:
                            department = self.env['hr.department'].create({'name': dept_name})
                        vals['department_id'] = department.id

            # 2. Hiérarchie principale avec création forcée
            hierarchy = [
                ('domain_id', 'qctracker.domain.project', None),
                ('process_id', 'qctracker.process.project', 'domain_id'),
                ('sub_process_id', 'qctracker.sub_process.project', 'process_id'),
                ('activity_id', 'qctracker.activity.project', 'sub_process_id'),
                ('procedure_id', 'qctracker.procedure.project', 'activity_id'),
                ('deliverable_id', 'qctracker.deliverable.project', 'procedure_id'),
                ('task_formulation_id', 'qctracker.task_formulation.project', 'procedure_id'),
            ]

            # D'abord créer tous les éléments de base
            created_records = {}
            for field, model, parent_field in hierarchy:
                if field in vals and vals[field]:
                    if isinstance(vals[field], (int, float)):
                        record = self.env[model].browse(int(vals[field]))
                        if not record.exists():
                            record = self.env[model].create({
                                'name': f"GENERATED-{field}-{vals[field]}"
                            })
                    else:
                        name = str(vals[field]).strip()
                        if name:
                            record = self.env[model].search([('name', '=ilike', name)], limit=1)
                            if not record:
                                create_vals = {'name': name}
                                if parent_field and parent_field in created_records:
                                    create_vals[parent_field] = created_records[parent_field].id
                                record = self.env[model].create(create_vals)

                    created_records[field] = record
                    vals[field] = record.id

            # 3. Vérification et correction des relations hiérarchiques
            for field, model, parent_field in hierarchy:
                if field in created_records and parent_field and parent_field in hierarchy:
                    current_record = created_records[field]
                    parent_record = created_records.get(parent_field)

                    if parent_record:
                        # Force la relation parent-enfant si nécessaire
                        if model == 'qctracker.process.project':
                            if current_record.domain_id != parent_record:
                                current_record.write({'domain_id': parent_record.id})
                        elif model == 'qctracker.sub_process.project':
                            if current_record.process_id != parent_record:
                                current_record.write({'process_id': parent_record.id})
                        # ... (autres relations à vérifier de la même manière)

            # 4. Valeurs par défaut et finalisation
            if not vals.get('name'):
                vals['name'] = 'Nouveau Projet de Processus'

            if 'domain_id' not in vals or not vals['domain_id']:
                vals['domain_id'] = self.env['qctracker.domain.project'].create({
                    'name': 'DOMAINE-PAR-DEFAUT'
                }).id

            return vals

        except Exception as e:
            # Solution de dernier recours
            error_name = f"ERREUR-IMPORT-{fields.Datetime.now()}"
            default_domain = self.env['qctracker.domain.project'].search([], limit=1) or \
                             self.env['qctracker.domain.project'].create({'name': 'DOMAINE-ERREUR'})

            return {
                'name': error_name,
                'domain_id': default_domain.id,
                'active': False,
                'notes': f"Erreur critique lors de l'import: {str(e)}"
            }