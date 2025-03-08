# -*- coding: utf-8 -*-
{
    'name': "qctracker",

    'summary': """
        Manage employee details, departments, projects, tasks, and performance evaluations in one integrated system.""",

    'description': """
        QC Tracker is an odoo module that makes management and projects follow up
    """,

    'author': "Qualisys Consulting",
    'website': "https://qualisysconsulting.com/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
