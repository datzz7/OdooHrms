# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    
    shipping_status = fields.Many2one(comodel_name='po.shipping.status', string="Shipping Status", related='purchase_id.shipping_status')
    tracking_number = fields.Char(string="Tracking Number", related='purchase_id.tracking_number')
   