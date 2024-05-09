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

from odoo import models


class StockBackorderConfirmation(models.TransientModel):
    _inherit = 'stock.backorder.confirmation'

    def process_cancel_backorder(self):
        cancel_backorder = super(StockBackorderConfirmation, self).process_cancel_backorder()

        # Create Unserved Stock List
        for pick_id in self.pick_ids:
            for move_id in pick_id.move_ids_without_package:
                sale_id = self.env['sale.order'].search([('name', '=', pick_id.origin)])
                price_unit = 0.0
                for order_line in sale_id.order_line:
                    if move_id.product_id == order_line.product_id:
                        price_unit = order_line.price_unit
                if (move_id.product_uom_qty - move_id.quantity_done) != 0:
                    vals = {'product_id': move_id.product_id.id,
                            'picking_ref_id': pick_id.id,
                            'warehouse_id': pick_id.picking_type_id.warehouse_id.id,
                            'partner_id': pick_id.partner_id.id,
                            'unserved_qty': move_id.product_uom_qty - move_id.quantity_done,
                            'so_ref': pick_id.origin,
                            'product_uom': move_id.product_uom.id,
                            'price_unit': price_unit if sale_id else 0.00,
                            }
                    self.env['unserved.stock.list'].create(vals)

        return cancel_backorder

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4
