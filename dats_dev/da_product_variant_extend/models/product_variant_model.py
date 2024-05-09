# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductModel(models.Model):
    _name = 'product.variant.model'

    name = fields.Char(string="Model", required=True)
    code = fields.Char(string="Code")
    is_active = fields.Boolean(string="Is active", default="True")
