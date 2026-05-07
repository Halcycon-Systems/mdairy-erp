# -*- coding: utf-8 -*-
# from odoo import http


# class FarmerManagement(http.Controller):
#     @http.route('/farmer_management/farmer_management', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/farmer_management/farmer_management/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('farmer_management.listing', {
#             'root': '/farmer_management/farmer_management',
#             'objects': http.request.env['farmer_management.farmer_management'].search([]),
#         })

#     @http.route('/farmer_management/farmer_management/objects/<model("farmer_management.farmer_management"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('farmer_management.object', {
#             'object': obj
#         })

