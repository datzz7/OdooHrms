# -*- coding: utf-8 -*-
#################################################################################
# Author      : Acespritech Solutions Pvt. Ltd. (<www.acespritech.com>)
# Copyright(c): 2012-Present Acespritech Solutions Pvt. Ltd.
# All Rights Reserved.
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#################################################################################

from odoo import api, fields, models


class UnservedStockList(models.Model):
    _name = "unserved.stock.list"
    _description = "Unserved Stock List"

    product_id = fields.Many2one(comodel_name='product.product', string='Product',
                                 ondelete='cascade')
    company_id = fields.Many2one(comodel_name='res.company', string='Company', required=True,
                                 default=lambda self: self.env.company)
    picking_ref_id = fields.Many2one(comodel_name='stock.picking', string='Picking Reference')
    warehouse_id = fields.Many2one(comodel_name='stock.warehouse', string='Warehouse')
    partner_id = fields.Many2one(comodel_name='res.partner', string='Customer')
    so_ref = fields.Char(string="SO Reference")
    unserved_qty = fields.Float(string='Unserved Qty', default=0.0)
    product_uom = fields.Many2one(comodel_name='uom.uom', string='UOM')
    price_unit = fields.Float(string='Unit Price', digits=0)
    unserved_amount = fields.Float(string='Unserved Amount', default=0.0, store=True,
                                   compute='_compute_unserved_amount')

    @api.depends('unserved_qty', 'price_unit')
    def _compute_unserved_amount(self):
        for line in self:
            line.unserved_amount = line.unserved_qty * line.price_unit if line.unserved_qty else 0.0

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4
