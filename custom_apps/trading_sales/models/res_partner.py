# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    is_salesman = fields.Boolean(default=False)
    is_encoder = fields.Boolean(default=False)
    registered_name = fields.Boolean(string="With Registered Name", default=False)
    registered_name_id = fields.One2many(comodel_name='registered.name',inverse_name='res_partner_id')