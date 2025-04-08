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
from odoo import http
from odoo.http import request

class DashController(http.Controller):

    @http.route('/dashboard/dash/', type='http', auth='user', website=True)
    def serve_dash(self, **kwargs):
        """Affiche une page avec une iframe pour intégrer Dash dans Odoo"""
        return request.render('qctracker.qctracker_dashboard_view', {
            'dash_url': "http://127.0.0.1:8050/dash/"
        })