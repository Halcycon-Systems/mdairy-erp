# -*- coding: utf-8 -*-
{
    'name': 'mDairy SMS Notifications',
    'version': '16.0.1.0.0',
    'summary': 'SMS notifications for farmers via Africa\'s Talking or Twilio',
    'description': """
mDairy SMS
==========
Manages:
- SMS notifications to farmers (collection confirmations, payout alerts)
- Configurable SMS gateway (Africa's Talking, Twilio)
- SMS templates
- Delivery tracking
    """,
    'category': 'Agriculture',
    'author': 'mDairy Team',
    'license': 'LGPL-3',
    'depends': ['mdairy_finance'],
    'data': [
        'security/ir.model.access.csv',
        'views/sms_views.xml',
        'views/sms_menus.xml',
        'data/sms_templates.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
