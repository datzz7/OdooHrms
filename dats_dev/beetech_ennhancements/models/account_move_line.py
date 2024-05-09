# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'
    
    brand_id = fields.Many2one(related="product_id.brand_id", string="Brand", copy=False)
    size_id = fields.Many2one(related="product_id.size_id",string="Size", copy=False)
    style_id = fields.Many2one(related="product_id.style_id", string="Style", copy=False)
    color_id = fields.Many2one(related="product_id.color_id", string="Color", copy=False)