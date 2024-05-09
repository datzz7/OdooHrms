# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    variant_model_id = fields.Many2one(comodel_name='product.variant.model', string="Model")
    variant_warranty_id = fields.Many2one(comodel_name='product.variant.warranty', string="Warranty")
    

class ProductProduct(models.Model):
    _inherit = 'product.product'

    variant_model_id = fields.Many2one(comodel_name='product.variant.model', string="Model")
    variant_warranty_id = fields.Many2one(comodel_name='product.variant.warranty', string="Warranty")