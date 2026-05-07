# -*- coding: utf-8 -*-
# from odoo import http


# class AccessControl(http.Controller):
#     @http.route('/access_control/access_control', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/access_control/access_control/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('access_control.listing', {
#             'root': '/access_control/access_control',
#             'objects': http.request.env['access_control.access_control'].search([]),
#         })

#     @http.route('/access_control/access_control/objects/<model("access_control.access_control"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('access_control.object', {
#             'object': obj
#         })

