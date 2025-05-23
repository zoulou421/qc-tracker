# -*- coding: utf-8 -*-
{
    'name': "QC Tracker",
    'summary': "Quality Control Project and Task Management System",
    'description': """
        Comprehensive Quality Control tracking system with:
        - Employee and department management
        - Project and task tracking
        - Performance evaluation
        - Reporting and analytics
    """,
    'author': "Qualisys Consulting",
    'website': "https://qualisysconsulting.com/",
    'category': 'Quality Control', # Simplified category
    'version': '0.1',
    'depends': ['base','web','project','hr','mail'],
    'data': [
        'security/qctracker_security.xml',
        'security/ir.model.access.csv',
        'data/qctracker_project_category_data.xml',
        'data/qctracker_project_category_internal_data.xml',
        'data/qctracker_process_data.xml',
        'data/workflow_data.xml',
        'views/qctracker_employee_view.xml',
        'views/qctracker_project_view.xml',
        'views/qctracker_task_view.xml',
        'views/qctracker_process_project_views.xml',
        'views/qctracker_department_view.xml',
        'views/qctracker_sub_task_view.xml',
        'views/qctracker_employee_rating_view.xml',
        'views/qctracker_project_delivery_view.xml',
        'views/qctracker_skill_view.xml',
        # 'views/qctracker_notification_views.xml',
        'views/qctracker_tag_views.xml',
        #'views/dashboard_v0.xml',
        'views/qctracker_actions.xml',
        'views/qctracker_menus.xml',
        #'views/assets.xml',  # Assets (CSS/JS) for the dashboard
        # 'views/views.xml',
        #'views/email_templates.xml',
        # 'views/templates.xml', # keep if needed otherwise remove.
        'views/hr_department_view.xml',
        'views/qctracker_process_importer_views.xml',
        'views/file_import_export.xml',
    ],
    'external_dependencies': {'python': ['openpyxl']},

    'demo': [
        'demo/demo.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'qctracker/static/src/css/fix_kanban.scss',
            'qctracker/static/src/css/employee_styles.css',
            'qctracker/static/src/js/employee_scripts.js',
            # 'qctracker/static/src/js/notification_badge.js',
            # 'qctracker/static/src/xml/notification_badge.xml',
        ],
        'web.assets_common': [
            # Optional: Add if hosting Animate.css locally
            # 'qctracker/static/src/css/animate.min.css',
        ],
    },
    'images': [],
    'installable': True,
    'application': True,
    'license': 'LGPL-3', #Added license.
}