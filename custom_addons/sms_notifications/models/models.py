# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class sms_notifications(models.Model):
#     _name = 'sms_notifications.sms_notifications'
#     _description = 'sms_notifications.sms_notifications'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

