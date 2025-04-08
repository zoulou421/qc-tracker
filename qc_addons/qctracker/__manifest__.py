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
        'views/qctracker_employee_view.xml',
        'views/qctracker_project_view.xml',
        'views/qctracker_task_view.xml',
        'views/qctracker_department_view.xml',
        'views/qctracker_sub_task_view.xml',
        'views/qctracker_employee_rating_view.xml',
        'views/qctracker_project_delivery_view.xml',
        'views/qctracker_skill_view.xml',
        #'views/dashboard_v0.xml',
        'views/qctracker_actions.xml',
        'views/qctracker_menus.xml',
        #'views/assets.xml',  # Assets (CSS/JS) for the dashboard
        # 'views/views.xml',
        #'views/email_templates.xml',
        # 'views/templates.xml', # keep if needed otherwise remove.
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'assets': {
        'web.assets_backend': [
            #'qctracker/static/src/css/dashboard.css',
            #'qctracker/static/src/js/dashboard.js',
            #'qctracker/static/src/css/dash.css',
            #'qctracker/static/src/js/dash.js',
            #'https://cdn.jsdelivr.net/npm/chart.js',
            #'qctracker/static/src/js/helper.js',
            #'qctracker/static/src/js/dashboard.js',
            #'qctracker/static/src/xml/dashboard.xml',
        ],
    },
    'images': [],
    'installable': True,
    'application': True,
    'license': 'LGPL-3', #Added license.
}