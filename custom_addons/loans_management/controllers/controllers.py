# -*- coding: utf-8 -*-
# from odoo import http


# class LoansManagement(http.Controller):
#     @http.route('/loans_management/loans_management', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/loans_management/loans_management/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('loans_management.listing', {
#             'root': '/loans_management/loans_management',
#             'objects': http.request.env['loans_management.loans_management'].search([]),
#         })

#     @http.route('/loans_management/loans_management/objects/<model("loans_management.loans_management"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('loans_management.object', {
#             'object': obj
#         })

