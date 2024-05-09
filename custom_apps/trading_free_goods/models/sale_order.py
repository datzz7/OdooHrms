# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    with_free_goods = fields.Boolean(string="With Free Goods?", default=False)
    free_goods_line_ids = fields.One2many(comodel_name='sale.order.free.goods.lines', inverse_name='sale_id', tracking=True)