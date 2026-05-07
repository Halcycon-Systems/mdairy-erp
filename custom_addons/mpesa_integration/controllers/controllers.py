# -*- coding: utf-8 -*-
# from odoo import http


# class MpesaIntegration(http.Controller):
#     @http.route('/mpesa_integration/mpesa_integration', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mpesa_integration/mpesa_integration/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('mpesa_integration.listing', {
#             'root': '/mpesa_integration/mpesa_integration',
#             'objects': http.request.env['mpesa_integration.mpesa_integration'].search([]),
#         })

#     @http.route('/mpesa_integration/mpesa_integration/objects/<model("mpesa_integration.mpesa_integration"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mpesa_integration.object', {
#             'object': obj
#         })

