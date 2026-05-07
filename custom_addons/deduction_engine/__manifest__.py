# -*- coding: utf-8 -*-
{
    'name': "Dairy Societies Management System - Deduction Engine",

    'summary': "Rule-based deductions for loans, feed, and recoveries.",

    'description': """
Deduction logic for the Dairy Societies Management System.
This module is intended to apply prioritized, traceable,
and partially recoverable deductions at farmer level.
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
