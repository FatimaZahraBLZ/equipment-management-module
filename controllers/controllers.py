# -*- coding: utf-8 -*-
# from odoo import http


# class GestionEquipements(http.Controller):
#     @http.route('/gestion_equipements/gestion_equipements', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/gestion_equipements/gestion_equipements/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('gestion_equipements.listing', {
#             'root': '/gestion_equipements/gestion_equipements',
#             'objects': http.request.env['gestion_equipements.gestion_equipements'].search([]),
#         })

#     @http.route('/gestion_equipements/gestion_equipements/objects/<model("gestion_equipements.gestion_equipements"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('gestion_equipements.object', {
#             'object': obj
#         })

