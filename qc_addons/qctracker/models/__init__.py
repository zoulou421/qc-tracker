# -*- coding: utf-8 -*-

import logging

_logger = logging.getLogger(__name__)
_logger.info("Loading QCTracker models")

from . import qc_tracker_employee
from . import qc_tracker_department
from . import qc_tracker_employeeRating
from . import qc_tracker_project
from . import qc_tracker_project_delivery
from . import qc_tracker_task
from . import qc_tracker_subTask
from . import qc_tracker_skill
from . import qc_tracker_skill_rating
from . import qc_tracker_task_notification
from . import qc_tracker_dashboard
from . import qc_tracker_tag
from . import qc_tracker_project_category
from . import qctracker_activity_project
from . import qctracker_deliverable_project
from . import qctracker_domain_project
from . import qctracker_formulation_project
from . import qctracker_procedure_project
from . import qctracker_process_project
from . import qctracker_sub_process_project
from . import qc_tracker_hr_department

from . import qctracker_process_project_project

_logger.info("Loaded qctracker_process_project_project")

from . import import_qctracker_process_xlsx

_logger.info("Loaded import_qctracker_process_xlsx")
