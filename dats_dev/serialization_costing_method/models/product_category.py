# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ProductCategory(models.Model):
    _inherit = 'product.category'
    
    property_cost_method = fields.Selection(selection_add=[('serialization', "Serialization")], ondelete={'serialization': 'set default'})