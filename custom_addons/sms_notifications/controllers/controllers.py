# -*- coding: utf-8 -*-
# from odoo import http


# class SmsNotifications(http.Controller):
#     @http.route('/sms_notifications/sms_notifications', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sms_notifications/sms_notifications/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('sms_notifications.listing', {
#             'root': '/sms_notifications/sms_notifications',
#             'objects': http.request.env['sms_notifications.sms_notifications'].search([]),
#         })

#     @http.route('/sms_notifications/sms_notifications/objects/<model("sms_notifications.sms_notifications"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sms_notifications.object', {
#             'object': obj
#         })

