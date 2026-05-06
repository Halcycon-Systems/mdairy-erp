# -*- coding: utf-8 -*-
{
    'name': 'mDairy MPESA Integration',
    'version': '16.0.1.0.0',
    'summary': 'Safaricom MPESA B2C integration for farmer payouts',
    'description': """
mDairy MPESA Integration
========================
Manages:
- MPESA B2C (Business to Customer) payouts to farmers
- MPESA transaction tracking and reconciliation
- Callback handling for payment status updates
- Configuration for Daraja API credentials
    """,
    'category': 'Agriculture',
    'author': 'mDairy Team',
    'license': 'LGPL-3',
    'depends': ['mdairy_finance'],
    'data': [
        'security/ir.model.access.csv',
        'views/mpesa_views.xml',
        'views/mpesa_menus.xml',
        'data/mpesa_data.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
