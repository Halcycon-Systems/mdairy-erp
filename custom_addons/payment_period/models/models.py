# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class payment_period(models.Model):
#     _name = 'payment_period.payment_period'
#     _description = 'payment_period.payment_period'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

