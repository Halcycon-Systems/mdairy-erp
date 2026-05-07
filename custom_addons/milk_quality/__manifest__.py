# -*- coding: utf-8 -*-
{
    'name': "Dairy Societies Management System - Milk Quality",

    'summary': "Milk quality checks, validation, and acceptance status.",

    'description': """
Milk testing and validation for the Dairy Societies Management System.
This module is intended to capture quality readings and control
whether collected milk can move into downstream financial flows.
    """,

    'author': "Halcyon * KaribuWD",
    'website': "https://github.com/kirobi01/mdairy-erp",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Industries',
    'version': '17.0.1.0.0',

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
