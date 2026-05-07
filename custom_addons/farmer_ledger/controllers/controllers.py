# -*- coding: utf-8 -*-
# from odoo import http


# class FarmerLedger(http.Controller):
#     @http.route('/farmer_ledger/farmer_ledger', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/farmer_ledger/farmer_ledger/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('farmer_ledger.listing', {
#             'root': '/farmer_ledger/farmer_ledger',
#             'objects': http.request.env['farmer_ledger.farmer_ledger'].search([]),
#         })

#     @http.route('/farmer_ledger/farmer_ledger/objects/<model("farmer_ledger.farmer_ledger"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('farmer_ledger.object', {
#             'object': obj
#         })

