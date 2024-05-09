# -*- coding: utf-8 -*- 

from odoo import models, fields, api, _


class OverlandedGoods(models.Model):
    _name = 'picking.overlanded.goods.lines'
    _description = "Overlanded Goods Lines"
    
    picking_id = fields.Many2one(comodel_name='stock.picking',)
    product_id = fields.Many2one(comodel_name='product.product', string="Product", tracking=True)
    uom_id = fields.Many2one(comodel_name='uom.uom')
    quantity = fields.Float()