# -*- coding: utf-8 -*-
# from odoo import http


# class MilkCollection(http.Controller):
#     @http.route('/milk_collection/milk_collection', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/milk_collection/milk_collection/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('milk_collection.listing', {
#             'root': '/milk_collection/milk_collection',
#             'objects': http.request.env['milk_collection.milk_collection'].search([]),
#         })

#     @http.route('/milk_collection/milk_collection/objects/<model("milk_collection.milk_collection"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('milk_collection.object', {
#             'object': obj
#         })

