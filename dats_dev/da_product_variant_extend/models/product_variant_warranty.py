# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductWarranty(models.Model):
    _name = 'product.variant.warranty'

    name = fields.Char(string="Warranty", required=True)
    code = fields.Char(string="Code")
    is_active = fields.Boolean(string="Is active", default="True")
