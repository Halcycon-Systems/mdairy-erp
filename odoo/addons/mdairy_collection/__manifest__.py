# -*- coding: utf-8 -*-
{
    'name': 'mDairy Milk Collection',
    'version': '16.0.1.0.0',
    'summary': 'Milk collection recording and quality validation',
    'description': """
mDairy Milk Collection
======================
Manages:
- Daily milk collection sessions (morning / evening)
- Quantity recording per farmer
- Quality testing results
- Bulk tank readings
- Rejection tracking
    """,
    'category': 'Agriculture',
    'author': 'mDairy Team',
    'license': 'LGPL-3',
    'depends': ['mdairy_base'],
    'data': [
        'security/ir.model.access.csv',
        'views/collection_views.xml',
        'views/quality_views.xml',
        'views/collection_menus.xml',
        'data/collection_data.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
