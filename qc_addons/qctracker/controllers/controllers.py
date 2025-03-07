# -*- coding: utf-8 -*-
# from odoo import http


# class Qctracker(http.Controller):
#     @http.route('/qctracker/qctracker', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/qctracker/qctracker/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('qctracker.listing', {
#             'root': '/qctracker/qctracker',
#             'objects': http.request.env['qctracker.qctracker'].search([]),
#         })

#     @http.route('/qctracker/qctracker/objects/<model("qctracker.qctracker"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('qctracker.object', {
#             'object': obj
#         })
