# -*- coding: utf-8 -*-
# from odoo import http


# class AuditLog(http.Controller):
#     @http.route('/audit_log/audit_log', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/audit_log/audit_log/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('audit_log.listing', {
#             'root': '/audit_log/audit_log',
#             'objects': http.request.env['audit_log.audit_log'].search([]),
#         })

#     @http.route('/audit_log/audit_log/objects/<model("audit_log.audit_log"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('audit_log.object', {
#             'object': obj
#         })

