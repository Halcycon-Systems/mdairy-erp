# -*- coding: utf-8 -*-
{
    'name': 'mDairy Finance & Payouts',
    'version': '16.0.1.0.0',
    'summary': 'Financial processing and farmer payouts',
    'description': """
mDairy Finance
==============
Manages:
- Monthly / periodic payout computation
- Deductions (loans, levies, insurance)
- Payout approval and disbursement
- Financial reports
    """,
    'category': 'Agriculture',
    'author': 'mDairy Team',
    'license': 'LGPL-3',
    'depends': ['mdairy_collection'],
    'data': [
        'security/ir.model.access.csv',
        'views/payout_views.xml',
        'views/deduction_views.xml',
        'views/finance_menus.xml',
        'data/finance_data.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
