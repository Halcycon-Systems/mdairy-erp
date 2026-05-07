# -*- coding: utf-8 -*-
# from odoo import http


# class PayoutProcessing(http.Controller):
#     @http.route('/payout_processing/payout_processing', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/payout_processing/payout_processing/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('payout_processing.listing', {
#             'root': '/payout_processing/payout_processing',
#             'objects': http.request.env['payout_processing.payout_processing'].search([]),
#         })

#     @http.route('/payout_processing/payout_processing/objects/<model("payout_processing.payout_processing"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('payout_processing.object', {
#             'object': obj
#         })

