# -*- coding: utf-8 -*-
import logging
import openpyxl
import os
import glob
import shutil
import platform
import zipfile
import re
from pathlib import Path
from odoo import models, api, fields
from odoo.exceptions import UserError, ValidationError
from odoo.tools import config

_logger = logging.getLogger(__name__)


class QCTrackerProcessImporter(models.TransientModel):
    _name = 'qctracker.process.importer'
    _description = 'Importateur de Projets de Processus QCTracker (XLSX)'

    file = fields.Binary(string="Fichier XLSX", help="Téléchargez un fichier XLSX à importer")
    file_name = fields.Char(string="Nom du fichier")

    def _get_base_dir(self):
        """Retourne le répertoire de base pour les fichiers, configurable via ir.config_parameter."""
        base_dir = self.env['ir.config_parameter'].sudo().get_param('qctracker.import_base_dir')
        if not base_dir:
            system = platform.system()
            if system == 'Windows':
                base_dir = Path('C:/Odoo/data')
            else:
                base_dir = Path(config.get('data_dir', '/home/odoo'))
                if not base_dir.exists():
                    base_dir = Path.home() / 'odoo'
        return Path(base_dir)

    def _sanitize_filename(self, filename):
        """Nettoie le nom du fichier pour supprimer les caractères problématiques."""
        # Remplacer les caractères non-alphanumériques (sauf . et -) par _
        sanitized = re.sub(r'[^\w\.-]', '_', filename)
        # Limiter la longueur à 100 caractères
        return sanitized[:100]

    def _validate_xlsx_file(self, file_path):
        """Valide que le fichier est un XLSX valide."""
        file_path = Path(file_path)  # Convertir en Path si ce n'est pas déjà fait
        _logger.debug(f"Validation du fichier: {file_path}")
        if not file_path.is_file():
            raise UserError(f"Le chemin {file_path} n'est pas un fichier valide.")
        if file_path.suffix.lower() != '.xlsx':
            raise UserError(f"Le fichier {file_path} doit être au format XLSX.")
        file_size = file_path.stat().st_size
        _logger.debug(f"Taille du fichier: {file_size} octets")
        if file_size < 1024:  # Fichier trop petit pour être un XLSX valide
            raise UserError(f"Le fichier {file_path} est trop petit ({file_size} octets) pour être un XLSX valide.")
        try:
            with zipfile.ZipFile(file_path, 'r') as zf:
                zf.testzip()  # Vérifie l'intégrité du ZIP
        except zipfile.BadZipFile:
            raise UserError(f"Le fichier {file_path} n'est pas un fichier XLSX valide (format ZIP corrompu).")
        except Exception as e:
            raise UserError(f"Erreur lors de la validation du fichier {file_path}: {str(e)}")

    def import_process_projects_xlsx(self, xlsx_file_path):
        """Importe des projets de processus à partir d'un fichier XLSX."""
        _logger.info(f"Tentative d'importation du fichier: {xlsx_file_path}")
        try:
            # Valider le fichier
            self._validate_xlsx_file(xlsx_file_path)

            # Vérifier l'installation d'openpyxl
            if not openpyxl:
                raise UserError("La bibliothèque 'openpyxl' n'est pas installée. Exécutez 'pip install openpyxl'.")

            # Vérifier l'accès au fichier
            if not os.access(xlsx_file_path, os.R_OK):
                raise UserError(f"Permission refusée pour lire le fichier: {xlsx_file_path}")

            # Charger le fichier XLSX
            _logger.debug(f"Chargement du fichier XLSX: {xlsx_file_path}")
            workbook = openpyxl.load_workbook(xlsx_file_path, read_only=True)
            sheet = workbook.active
            if not sheet:
                raise UserError(f"Le fichier XLSX {xlsx_file_path} ne contient aucune feuille.")

            # Extraire les en-têtes (première ligne)
            headers = [cell.value for cell in next(sheet.rows) if cell.value is not None]
            if not headers:
                raise UserError(f"Le fichier XLSX {xlsx_file_path} n'a pas d'en-têtes valides.")
            _logger.debug(f"En-têtes trouvés: {headers}")

            # Mapper les en-têtes aux champs Odoo
            header_mapping = {
                'Nom': 'name',
                'Domaine': 'domain_id',
                'Processus': 'process_id',
                'Sous-processus': 'sub_process_id',
                'Activité': 'activity_id',
                'Procédure': 'procedure_id',
                'Livrable': 'deliverable_id',
                'Formulation des Tâches': 'task_formulation_id',
                'Responsable': 'employee_id',
                'Département': 'department_id',
                'Notes': 'notes',
            }

            # Vérifier que les en-têtes nécessaires sont présents
            required_headers = ['Domaine', 'Processus', 'Sous-processus', 'Activité',
                                'Procédure', 'Livrable', 'Formulation des Tâches']
            missing_headers = [h for h in required_headers if h not in headers]
            if missing_headers:
                raise UserError(f"En-têtes manquants dans le fichier XLSX: {', '.join(missing_headers)}")

            process_model = self.env['qctracker.process.project.project']
            errors = []
            imported_count = 0

            # Parcourir les lignes de données
            for row_idx, row in enumerate(sheet.iter_rows(min_row=2, values_only=True), start=2):
                try:
                    # Ignorer les lignes vides
                    if all(cell is None for cell in row):
                        continue

                    # Créer un dictionnaire des valeurs
                    vals = {}
                    for idx, value in enumerate(row):
                        if idx < len(headers) and headers[idx] in header_mapping:
                            field = header_mapping[headers[idx]]
                            vals[field] = str(value).strip() if value is not None else ''

                    # Assurer un nom par défaut
                    if not vals.get('name'):
                        vals['name'] = 'Nouveau Projet de Processus'

                    # Vérifier les champs obligatoires
                    if not vals.get('deliverable_id'):
                        errors.append(f"Ligne {row_idx}: Le champ 'Livrable' est requis.")
                        continue

                    # Nettoyer les valeurs vides
                    vals = {k: v for k, v in vals.items() if v}

                    # Créer l'enregistrement
                    process_model.create(vals)
                    imported_count += 1
                    _logger.info(f"Enregistrement créé (ligne {row_idx}): {vals.get('name')}")

                except Exception as e:
                    errors.append(f"Ligne {row_idx}: {str(e)}")
                    _logger.error(f"Erreur à la ligne {row_idx}: {str(e)}")
                    continue

            # Journaliser le résumé
            summary = f"Importation terminée pour {xlsx_file_path}: {imported_count} enregistrements importés."
            if errors:
                summary += f" {len(errors)} erreurs:\n" + "\n".join(errors)
                _logger.warning(summary)
                # Créer une activité Odoo pour signaler les erreurs
                self._create_error_activity(xlsx_file_path, errors)
            else:
                _logger.info(summary)

            return imported_count, errors

        except Exception as e:
            _logger.error(f"Erreur lors de l'ouverture du fichier XLSX {xlsx_file_path}: {str(e)}")
            raise UserError(f"Erreur lors du traitement du fichier XLSX: {str(e)}")
        finally:
            if 'workbook' in locals():
                workbook.close()

    def _create_error_activity(self, file_path, errors):
        """Crée une activité Odoo pour signaler les erreurs d'importation."""
        admin_user = self.env.ref('base.user_admin')
        self.env['mail.activity'].create({
            'res_model_id': self.env['ir.model']._get('qctracker.process.importer').id,
            'res_id': self.id,
            'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
            'summary': f"Erreurs lors de l'importation de {os.path.basename(file_path)}",
            'note': f"{len(errors)} erreurs rencontrées:\n" + "\n".join(errors),
            'user_id': admin_user.id,
        })

    def action_import_uploaded_file(self):
        """Importe un fichier XLSX téléchargé via l'interface Odoo."""
        if not self.file:
            raise UserError("Veuillez télécharger un fichier XLSX.")
        if not self.file_name.endswith('.xlsx'):
            raise UserError("Le fichier doit être au format XLSX.")

        # Enregistrer le fichier temporairement
        base_dir = self._get_base_dir()
        temp_dir = base_dir / 'temp'
        temp_dir.mkdir(parents=True, exist_ok=True)
        sanitized_filename = self._sanitize_filename(self.file_name)
        temp_file_path = temp_dir / sanitized_filename

        _logger.info(f"Enregistrement du fichier temporaire: {temp_file_path} (original: {self.file_name})")
        try:
            with open(temp_file_path, 'wb') as f:
                f.write(self.file)
            # Valider le fichier avant importation
            self._validate_xlsx_file(temp_file_path)
            # Importer le fichier
            imported_count, errors = self.import_process_projects_xlsx(temp_file_path)
            # Retourner un message à l'utilisateur
            message = f"Importation terminée: {imported_count} enregistrements importés."
            if errors:
                message += f" {len(errors)} erreurs rencontrées. Consultez les activités pour plus de détails."
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Importation XLSX',
                    'message': message,
                    'type': 'success' if not errors else 'warning',
                    'sticky': True,
                }
            }
        except Exception as e:
            _logger.error(f"Erreur lors de l'importation manuelle: {str(e)}")
            raise UserError(f"Erreur lors de l'importation: {str(e)}")
        finally:
            # Supprimer le fichier temporaire
            if temp_file_path.exists():
                os.remove(temp_file_path)
                _logger.debug(f"Fichier temporaire supprimé: {temp_file_path}")

    @api.model
    def run_scheduled_import_xlsx(self):
        """Tâche planifiée pour importer des fichiers XLSX depuis un répertoire."""
        base_dir = self._get_base_dir()
        import_dir = base_dir / 'import' / 'xlsx'
        archive_dir = base_dir / 'archive' / 'xlsx'
        error_dir = base_dir / 'error' / 'xlsx'

        # Créer les répertoires s'ils n'existent pas
        for directory in [import_dir, archive_dir, error_dir]:
            directory = Path(directory)
            if not directory.exists():
                try:
                    directory.mkdir(parents=True, exist_ok=True)
                    _logger.info(f"Répertoire créé: {directory}")
                except Exception as e:
                    _logger.error(f"Erreur lors de la création du répertoire {directory}: {str(e)}")
                    raise UserError(f"Impossible de créer le répertoire {directory}: {str(e)}")

        # Trouver tous les fichiers XLSX
        xlsx_files = glob.glob(os.path.join(import_dir, '*.xlsx'))
        if not xlsx_files:
            _logger.info("Aucun fichier XLSX trouvé dans le répertoire d'importation.")
            return

        for xlsx_file in xlsx_files:
            _logger.info(f"Traitement du fichier dans l'importation planifiée: {xlsx_file}")
            try:
                # Vérifier les permissions d'écriture pour le déplacement
                for dest_dir in [archive_dir, error_dir]:
                    if not os.access(dest_dir, os.W_OK):
                        raise UserError(f"Permission refusée pour écrire dans le répertoire: {dest_dir}")

                # Valider le fichier
                self._validate_xlsx_file(xlsx_file)
                imported_count, errors = self.import_process_projects_xlsx(xlsx_file)
                # Déplacer le fichier vers l'archive ou le répertoire d'erreur
                dest_dir = error_dir if errors else archive_dir
                shutil.move(xlsx_file, os.path.join(dest_dir, os.path.basename(xlsx_file)))
                _logger.info(f"Fichier traité: {xlsx_file} -> Déplacé vers {dest_dir}")
            except Exception as e:
                _logger.error(f"Erreur critique lors du traitement de {xlsx_file}: {str(e)}")
                # Déplacer vers le répertoire d'erreur
                try:
                    shutil.move(xlsx_file, os.path.join(error_dir, os.path.basename(xlsx_file)))
                    _logger.info(f"Fichier en erreur déplacé: {xlsx_file} -> {error_dir}")
                except Exception as move_e:
                    _logger.error(f"Erreur lors du déplacement de {xlsx_file} vers {error_dir}: {str(move_e)}")
                continue


# --- MODÈLE workflow.hierarchy (inchangé par rapport à la dernière version M2M) ---
class WorkflowHierarchy(models.Model):
    _name = 'workflow.hierarchy'
    _description = 'Gestion de la hiérarchie Domaine-Processus-Activité (Many2many)'

    name = fields.Char(string='Nom de l\'entrée hiérarchique', required=True, default='Nouvelle entrée')

    domain_ids = fields.Many2many('workflow.domain', string='Domaines')
    process_ids = fields.Many2many('workflow.process', string='Processus')
    sub_process_ids = fields.Many2many('workflow.subprocess', string='Sous-processus')
    activity_ids = fields.Many2many('workflow.activity', string='Activités')

    notes = fields.Text(string='Notes')
    active = fields.Boolean(default=True)

    @api.model
    def _find_or_create_m2m_records(self, model_name, field_name_in_row):
        """
        Helper pour trouver ou créer des enregistrements Many2many.
        Gère les noms multiples séparés par des virgules.
        """
        record_ids = []
        names_str = self.env.context.get(field_name_in_row)

        if not names_str:
            return [(5, 0, 0)]  # Enlève toutes les relations si la chaîne est vide

        names = [name.strip() for name in names_str.split(',') if name.strip()]

        for name in names:
            record = self.env[model_name].search([('name', '=', name)], limit=1)
            if not record:
                _logger.info(f"Creating new {model_name}: {name}")
                try:
                    record = self.env[model_name].create({'name': name})
                except Exception as e:
                    _logger.error(f"Failed to create {model_name} '{name}': {e}", exc_info=True)
                    continue
            record_ids.append(record.id)

        return [(6, 0, record_ids)]

    @api.model
    def import_hierarchy(self, row):
        """
        Méthode pour importer ou mettre à jour une ligne de données avec des champs Many2many.
        Les valeurs Many2many doivent être une chaîne de caractères séparée par des virgules.
        """
        hierarchy_name = row.get('name', 'Nouvelle entrée')
        vals = {'name': hierarchy_name}

        try:
            # Gestion des Domaines (Many2many) - PAS DE PARENT ICI
            domain_names = row.get('domain')
            vals['domain_ids'] = self.with_context(domain=domain_names)._find_or_create_m2m_records(
                'workflow.domain', 'domain'
            )

            # Gestion des Processus (Many2many) - PAS DE PARENT ICI
            process_names = row.get('process')
            vals['process_ids'] = self.with_context(process=process_names)._find_or_create_m2m_records(
                'workflow.process', 'process'
            )

            # Gestion des Sous-processus (Many2many) - PAS DE PARENT ICI
            sub_process_names = row.get('sub_process')
            vals['sub_process_ids'] = self.with_context(sub_process=sub_process_names)._find_or_create_m2m_records(
                'workflow.subprocess', 'sub_process'
            )

            # Gestion des Activités (Many2many) - PAS DE PARENT ICI
            activity_names = row.get('activity')
            vals['activity_ids'] = self.with_context(activity=activity_names)._find_or_create_m2m_records(
                'workflow.activity', 'activity'
            )

            if 'notes' in row:
                vals['notes'] = row['notes']
            vals['active'] = row.get('active', '1') == '1'

            existing_hierarchy_entry = self.search([('name', '=', hierarchy_name)], limit=1)

            if existing_hierarchy_entry:
                _logger.info(f"Updating existing workflow hierarchy entry: {hierarchy_name}")
                existing_hierarchy_entry.write(vals)
                return existing_hierarchy_entry
            else:
                _logger.info(f"Creating new workflow hierarchy entry: {hierarchy_name}")
                return self.create(vals)

        except Exception as e:
            _logger.error(f"Error importing workflow hierarchy row: {row}. Error: {e}", exc_info=True)
            return self.create({
                'name': f"ERREUR-IMPORT-{hierarchy_name}",
                'notes': f"Failed to import: {row}. Error: {e}",
                'active': False,
            })


# --- MODÈLES workflow.domain, workflow.process, workflow.subprocess, workflow.activity ---
# --- AVEC DES RELATIONS MANY2MANY VERS LE HAUT ET SANS CONTRAINTES DE PARENTÉ ---

class WorkflowDomain(models.Model):
    _name = 'workflow.domain'
    _description = 'Domaines de workflow (Many2many vers le bas)'

    name = fields.Char(string='Nom du domaine', required=True)
    _sql_constraints = [('name_uniq', 'unique (name)', 'Le nom du domaine doit être unique !')]

    # Inverse relation (pas strictement nécessaire mais utile pour naviguer)
    process_ids = fields.Many2many('workflow.process', 'workflow_domain_process_rel', 'domain_id', 'process_id',
                                   string='Processus associés')


class WorkflowProcess(models.Model):
    _name = 'workflow.process'
    _description = 'Processus métier (Many2many vers le haut et le bas)'

    name = fields.Char(string='Nom du processus', required=True)
    _sql_constraints = [
        ('name_uniq', 'unique (name)', 'Le nom du processus doit être unique !')]  # Contrainte sur le nom seul

    # Champ Many2many vers les domaines (remplace le Many2one domain_id)
    domain_ids = fields.Many2many('workflow.domain', 'workflow_domain_process_rel', 'process_id', 'domain_id',
                                  string='Domaines associés')

    # Inverse relation vers les sous-processus
    sub_process_ids = fields.Many2many('workflow.subprocess', 'workflow_process_subprocess_rel', 'process_id',
                                       'subprocess_id', string='Sous-processus associés')


class WorkflowSubProcess(models.Model):
    _name = 'workflow.subprocess'
    _description = 'Sous-processus (Many2many vers le haut et le bas)'

    name = fields.Char(string='Nom du sous-processus', required=True)
    _sql_constraints = [
        ('name_uniq', 'unique (name)', 'Le nom du sous-processus doit être unique !')]  # Contrainte sur le nom seul

    # Champ Many2many vers les processus (remplace le Many2one process_id)
    process_ids = fields.Many2many('workflow.process', 'workflow_process_subprocess_rel', 'subprocess_id', 'process_id',
                                   string='Processus associés')

    # Inverse relation vers les activités
    activity_ids = fields.Many2many('workflow.activity', 'workflow_subprocess_activity_rel', 'subprocess_id',
                                    'activity_id', string='Activités associées')


class WorkflowActivity(models.Model):
    _name = 'workflow.activity'
    _description = 'Activités métier (Many2many vers le haut)'

    name = fields.Char(string="Nom de l'activité", required=True)
    _sql_constraints = [
        ('name_uniq', 'unique (name)', 'Le nom de l\'activité doit être unique !')]  # Contrainte sur le nom seul

    # Champ Many2many vers les sous-processus (remplace le Many2one sub_process_id)
    sub_process_ids = fields.Many2many('workflow.subprocess', 'workflow_subprocess_activity_rel', 'activity_id',
                                       'subprocess_id', string='Sous-processus associés')

