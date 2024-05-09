# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    with_free_goods = fields.Boolean(string='With free goods?', default=False)
    with_overlanded_goods = fields.Boolean(string='With Overlanded?', default=False)
    free_goods_line_ids = fields.One2many(comodel_name='picking.free.goods.lines', inverse_name='picking_id', copy=False)
    overlanded_goods_line_ids = fields.One2many(comodel_name='picking.overlanded.goods.lines', inverse_name='picking_id', copy=False)
    
    
    @api.model
    def create(self, vals):
        res = super(StockPicking, self).create(vals)
        sale_id = self.env['sale.order']
        for rec in res:
            if rec.origin:
                sale_id = sale_id.search([('name', '=', rec.origin)])
                if sale_id.with_free_goods == True:
                    rec.update({'with_free_goods': sale_id.with_free_goods})
                    for lines in sale_id.free_goods_line_ids:
                        rec.free_goods_line_ids.create({'picking_id': res.id,
                                              'product_id': lines.product_id.id,
                                               'uom_id': lines.uom_id.id,
                                               'quantity': lines.quantity
                                               })
        return res