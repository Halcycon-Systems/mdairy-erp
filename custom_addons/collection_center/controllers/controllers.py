# -*- coding: utf-8 -*-
# from odoo import http


# class CollectionCenter(http.Controller):
#     @http.route('/collection_center/collection_center', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/collection_center/collection_center/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('collection_center.listing', {
#             'root': '/collection_center/collection_center',
#             'objects': http.request.env['collection_center.collection_center'].search([]),
#         })

#     @http.route('/collection_center/collection_center/objects/<model("collection_center.collection_center"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('collection_center.object', {
#             'object': obj
#         })

