# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class KsRMA(models.Model):
    _inherit = "ks.rma"
   
    
    def ks_purchase_refund_invoice(self):
        invoice_state_list = self.ks_purchase_order_id.invoice_ids.mapped('state')
        if 'posted' in invoice_state_list or 'paid' in invoice_state_list:
            line_list = []
            if self.ks_rma_line_ids:
                for rma_line in self.ks_rma_line_ids:
                    if rma_line.ks_refund_qty:
                        line_list.append(
                            (0, 0, {
                                'quantity': rma_line.ks_refund_qty,
                                'product_id': rma_line.ks_product_id.id,
                                'price_unit': rma_line.ks_price_unit,
                                'tax_ids': [(6, 0, rma_line.tax_ids.ids)],
                            }))
            refund_invoice_id = self.env['account.move'].create({
                'move_type': 'in_refund',
                'partner_id': self.ks_partner_id.id,
                'currency_id': self.ks_currency_id.id,
                'invoice_line_ids': line_list,
                'invoice_origin': self.ks_purchase_order_id.name,
                'invoice_date': self.ks_date_confirmed,
            })
            if refund_invoice_id:
                for line in refund_invoice_id.invoice_line_ids:
                    line.name = line._get_computed_name()
                    line.account_id = line._get_computed_account()
                    line.product_uom_id = line._get_computed_uom()
                refund_invoice_id.action_post()
                return refund_invoice_id

    
    def _prepare_picking_receipt(self):
        stock_picking = self.env['stock.picking']
        line_ids = []
        stock_dict_sale = {
            'ks_rma_id': self.id,
            'is_rma_in_picking': True,
            'state': 'assigned',
            'origin': self.ks_get_picking,
            'partner_id': self.ks_partner_id.id,
            'picking_type_id': self.ks_return_picking_type_id.id,
            'company_id': self.ks_company_id.id,
            'location_id': self.ks_picking_id.location_dest_id.id,
            'location_dest_id': self.ks_picking_id.location_id.id
        }
        stock_picking = stock_picking.create(stock_dict_sale)
        for rma_line in self.ks_rma_line_ids:
            if rma_line.ks_returned_qty:
                line_ids.append(self.env['stock.move'].create({
                    'name': rma_line.ks_product_id.name if rma_line.ks_product_id else '',
                    'product_id': rma_line.ks_product_id.id if rma_line.ks_product_id else False,
                    'product_uom_qty': rma_line.ks_returned_qty,
                    'picking_id': stock_picking.id,
                    'product_uom': rma_line.ks_product_id.uom_id.id if rma_line.ks_product_id else False,
                    'location_id': self.ks_picking_id.location_dest_id.id,
                    'location_dest_id': self.ks_picking_id.location_id.id,
                    'lot_ids': [(6, 0, rma_line.lot_id.ids)] 
                }).id)
        return stock_picking

    def _prepare_picking_order(self):
        stock_picking = self.env['stock.picking']
        line_ids = []
        stock_dict_sale = {
            'ks_rma_id': self.id,
            'is_rma_out_picking': True,
            'state': 'assigned',
            'origin': self.ks_get_picking,
            'partner_id': self.ks_partner_id.id,
            'company_id': self.ks_company_id.id,
            'picking_type_id': self.ks_return_picking_type_id.id,
            'location_id': self.ks_picking_id.location_dest_id.id,
            'location_dest_id': self.ks_picking_id.location_id.id,
        }
        stock_picking = stock_picking.create(stock_dict_sale)
        for rma_line in self.ks_rma_line_ids:
            if rma_line.ks_returned_qty:
                move = self.env['stock.move'].create({
                    'name': rma_line.ks_product_id.name if rma_line.ks_product_id else '',
                    'product_id': rma_line.ks_product_id.id if rma_line.ks_product_id else False,
                    'product_uom_qty': rma_line.ks_returned_qty,
                    'picking_id': stock_picking.id,
                    'product_uom': rma_line.ks_product_id.uom_id.id if rma_line.ks_product_id else False,
                    'location_id': self.ks_picking_id.location_dest_id.id,
                    'location_dest_id': self.ks_picking_id.location_id.id,
                    'lot_ids': [(6, 0,  rma_line.lot_id.ids)] 
                })
                line_ids.append(move.id)
                # move_line_vals = [(0, 0, {
                #     'product_id': rma_line.ks_product_id.id,
                #     'location_id': self.ks_picking_id.location_dest_id.id,
                #     'location_dest_id': self.ks_picking_id.location_id.id,
                #     'lot_id': rma_line.lot_id.id,
                #     # 'qty_done': rma_line.ks_returned_qty,
                #     'product_uom_qty': rma_line.ks_returned_qty,
                #     'lot_name':  rma_line.lot_id.name,
                #     'product_uom_id': rma_line.ks_product_id.uom_id.id,
                #     'picking_id': stock_picking.id,
                # })]
                # move.update({'move_line_ids': move_line_vals})
                move.move_line_ids.update({'product_uom_qty': rma_line.ks_returned_qty})
        return stock_picking
    
    @api.onchange('ks_picking_id')
    def _set_rma_line_ids_from_picking(self):
        if self.ks_picking_id:
            line_ids, tax_ids = [], []
            rma_product_price = {}
            price = 0
            discount = 0.0
            if not self.ks_picking_id.move_lines:
                self.update({
                    'ks_picking_id': False
                })
                raise UserError(_('Selected picking has no move line!! Please select another picking'))
            self.ks_picking_type_id = self.ks_picking_id.picking_type_id.id
            if self.ks_selection == 'transfer':
                self.ks_partner_id = self.ks_picking_id.partner_id.id
            if self.ks_selection == 'sale_order':
                rma_product_price = self._return_order_line_product_price_dict(self.ks_sale_order_id.order_line)
            if self.ks_selection == 'purchase_order':
                rma_product_price = self._return_order_line_product_price_dict(self.ks_purchase_order_id.order_line)
            for move_line in self.ks_picking_id.move_line_ids_without_package:
                if rma_product_price.get(move_line.product_id.id, False):
                    price = rma_product_price[move_line.product_id.id][0]
                    tax_ids = rma_product_price[move_line.product_id.id][1]
                    discount = rma_product_price[move_line.product_id.id][2]
                line_ids.append(self.env['ks.rma.line'].create({
                    'ks_product_id': move_line.product_id.id if move_line.product_id else False,
                    'ks_delivered_qty': move_line.qty_done,
                    'ks_price_unit': price,
                    'tax_ids': [(6, 0, tax_ids)],
                    'discount': discount,
                    'ks_company_id': self.ks_company_id.id,
                    'ks_returned_qty': move_line.qty_done if self.ks_is_return else 0,
                    'ks_refund_qty': move_line.qty_done if self.ks_is_refund else 0,
                    'ks_replace_qty': move_line.qty_done if self.ks_is_replace else 0,
                    'lot_id': move_line.lot_id.id
                }).id)
            self.ks_rma_line_ids = [(6, 0, line_ids)]

    def action_ks_rma_return(self):
        if self.state in ['confirm', 'refunded'] and self.ks_selection == 'sale_order':
            stock_picking_record = self._prepare_picking_receipt()
            if stock_picking_record:
                self.ks_return_picking_id = stock_picking_record
                if self.state == 'refunded':
                    self.state = 'refund_return'

        if self.state in ['confirm', 'refunded'] and self.ks_selection == 'purchase_order':
            stock_picking_record = self._prepare_picking_order()
            if stock_picking_record:
                self.ks_return_picking_id = stock_picking_record
                if self.state == 'refunded':
                    self.state = 'refund_return'
        if self.state == 'confirm' and self.ks_selection == 'transfer':
            if self.ks_picking_id.picking_type_id.code == 'incoming':
                stock_picking_record = self._prepare_picking_order()
                if stock_picking_record:
                    self.ks_return_picking_id = stock_picking_record
            if self.ks_picking_id.picking_type_id.code == 'outgoing':
                stock_picking_record = self._prepare_picking_receipt()
                if stock_picking_record:
                    self.ks_return_picking_id = stock_picking_record
            if self.ks_picking_id.picking_type_id.code == 'internal':
                stock_picking_record = self._prepare_picking_internal()
                if stock_picking_record:
                    self.ks_return_picking_id = stock_picking_record
                    
    @api.onchange('ks_sale_order_id', 'ks_purchase_order_id')
    def onchange_order_id(self):
        if self.ks_sale_order_id:
            self.ks_get_picking = self.ks_sale_order_id.name
            self.ks_partner_id = self.ks_sale_order_id.partner_id
        if self.ks_purchase_order_id:
            self.ks_get_picking = self.ks_purchase_order_id.name
            self.ks_partner_id = self.ks_purchase_order_id.partner_id
        if self.ks_selection == 'transfer':
            self.ks_get_picking = self.ks_picking_id.name
        return {'domain': {'ks_picking_id': [('partner_id', '=', self.ks_partner_id.id),
                                             ('origin', '=', self.ks_get_picking),
                                             ('state', '=', 'done')]
                           }}
        
    @api.onchange('ks_is_return')
    def _set_default_return_quantity(self):
        if self.ks_picking_id:
            for rma_line in self.ks_rma_line_ids:
                if self.ks_is_return:
                    rma_line.ks_returned_qty = 0
                else:
                    rma_line.ks_returned_qty = 0

    @api.onchange('ks_is_refund')
    def _set_default_refund_quantity(self):
        if self.ks_picking_id and self.ks_is_refund:
            for rma_line in self.ks_rma_line_ids:
                if self.ks_is_refund:
                    rma_line.ks_refund_qty = 0
                else:
                    rma_line.ks_refund_qty = 0

    @api.onchange('ks_is_replace')
    def _set_default_replace_quantity(self):
        if self.ks_picking_id and self.ks_is_replace:
            for rma_line in self.ks_rma_line_ids:
                if self.ks_is_replace:
                    rma_line.ks_replace_qty = 0
                else:
                    rma_line.ks_replace_qty = 0