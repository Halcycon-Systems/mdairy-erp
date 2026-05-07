# -*- coding: utf-8 -*-
# from odoo import http


# class PaymentPeriod(http.Controller):
#     @http.route('/payment_period/payment_period', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/payment_period/payment_period/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('payment_period.listing', {
#             'root': '/payment_period/payment_period',
#             'objects': http.request.env['payment_period.payment_period'].search([]),
#         })

#     @http.route('/payment_period/payment_period/objects/<model("payment_period.payment_period"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('payment_period.object', {
#             'object': obj
#         })

