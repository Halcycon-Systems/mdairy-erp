# -*- coding: utf-8 -*-
# from odoo import http


# class MilkQuality(http.Controller):
#     @http.route('/milk_quality/milk_quality', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/milk_quality/milk_quality/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('milk_quality.listing', {
#             'root': '/milk_quality/milk_quality',
#             'objects': http.request.env['milk_quality.milk_quality'].search([]),
#         })

#     @http.route('/milk_quality/milk_quality/objects/<model("milk_quality.milk_quality"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('milk_quality.object', {
#             'object': obj
#         })

