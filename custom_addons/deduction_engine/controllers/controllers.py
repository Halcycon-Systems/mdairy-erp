# -*- coding: utf-8 -*-
# from odoo import http


# class DeductionEngine(http.Controller):
#     @http.route('/deduction_engine/deduction_engine', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/deduction_engine/deduction_engine/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('deduction_engine.listing', {
#             'root': '/deduction_engine/deduction_engine',
#             'objects': http.request.env['deduction_engine.deduction_engine'].search([]),
#         })

#     @http.route('/deduction_engine/deduction_engine/objects/<model("deduction_engine.deduction_engine"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('deduction_engine.object', {
#             'object': obj
#         })

