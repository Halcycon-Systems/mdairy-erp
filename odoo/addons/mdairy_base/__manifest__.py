# -*- coding: utf-8 -*-
{
    'name': 'mDairy Base',
    'version': '16.0.1.0.0',
    'summary': 'Core module for mDairy ERP – farmer records and cooperative management',
    'description': """
mDairy Base
===========
Core module that manages:
- Farmer / supplier records
- Cooperative / collection centre records
- Basic configuration for the mDairy ERP system
    """,
    'category': 'Agriculture',
    'author': 'mDairy Team',
    'website': 'https://github.com/kirobi01/mdairy-erp',
    'license': 'LGPL-3',
    'depends': ['base', 'mail', 'product'],
    'data': [
        'security/ir.model.access.csv',
        'security/mdairy_security.xml',
        'views/farmer_views.xml',
        'views/cooperative_views.xml',
        'views/mdairy_menus.xml',
        'data/mdairy_data.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
