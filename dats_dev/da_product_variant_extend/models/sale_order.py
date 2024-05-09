# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
    variant_model_id = fields.Many2one(comodel_name='product.variant.model', string="Model",)
    variant_warranty_id = fields.Many2one(comodel_name='product.variant.warranty', string="Warranty",)
    
    @api.onchange('product_id')
    def _get_product_model_warranty(self):
        for rec in self:
            rec.variant_model_id = rec.product_id.variant_model_id.id
            rec.variant_warranty_id = rec.product_id.variant_warranty_id.id