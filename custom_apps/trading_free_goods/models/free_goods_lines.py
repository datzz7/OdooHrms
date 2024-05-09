# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SalesFreeGoodsLines(models.Model):
    _name = 'sale.order.free.goods.lines'
    _description = "Sale order free goods"
    
    
    sale_id = fields.Many2one(comodel_name='sale.order',)
    product_id = fields.Many2one(comodel_name='product.product', string="Product")
    uom_id = fields.Many2one(comodel_name='uom.uom')
    quantity = fields.Float()


class PickingFreeGoodsLines(models.Model):
    _name = 'picking.free.goods.lines'
    _description = "Stock Picking free goods"
    
    
    picking_id = fields.Many2one(comodel_name='stock.picking',)
    product_id = fields.Many2one(comodel_name='product.product', string="Product", tracking=True)
    uom_id = fields.Many2one(comodel_name='uom.uom')
    quantity = fields.Float()
    