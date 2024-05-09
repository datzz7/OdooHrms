# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

class AccountMove(models.Model):
    _inherit = 'account.move'
    
    or_number = fields.Char(string="OR No.", tracking=True)
    customer_po_no = fields.Char(string="PO No.", tracking=True)
    order_type = fields.Many2one(comodel_name='sales.order.type', string="Order Type", tracking=True)
    country_id = fields.Many2one(comodel_name='sales.area', string="Area",)
    partner_registered_names = fields.Many2one(comodel_name='registered.name', copy=False)
    price_list_id = fields.Many2one(comodel_name='product.pricelist', string="Pricelist")
    sales_type = fields.Selection(selection=[('booking', "Booking"),
                                            ('route', "Route")], string="Sales Type")
    
    @api.onchange('partner_id')
    def _onchange_partner_id_vat_change(self):
        for rec in self:
            if rec.partner_id:
                return {'domain': {'partner_registered_names': [('res_partner_id', '=', rec.partner_id.id)]}}
            else:
                return
            
    @api.onchange('price_list_id')
    def get_pricelist_price(self):
        self.invoice_line_ids._onchange_product_id_account_invoice_pricelist()
        self.with_context(check_move_validity=False)._recompute_dynamic_lines(
            recompute_all_taxes=True, recompute_tax_base_amount=True)

    @api.model
    def create(self, vals):
        origin = vals.get('invoice_origin')
        if origin:
            sale_obj = self.env['sale.order'].search([('name', '=', origin)])
            
            if sale_obj:
                for rec in sale_obj:
                    vals['sales_type'] = 'booking'
                    vals['price_list_id'] = rec.pricelist_id
                    vals['order_type'] = rec.order_type
                    vals['customer_po_no'] = rec.customer_po_no
                    vals['country_id'] = rec.country_id
                    vals['partner_registered_names'] = rec.partner_registered_names
                    
        res = super(AccountMove, self).create(vals)
        return res

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    m_price_list = fields.Many2one(
        comodel_name='product.pricelist', related='move_id.price_list_id')
   
    
    def _check_free_goods_module(self):
        account_move_line = self.env['account.move.line'].fields_get()
        trading_free_goods = False
        
        for field_name in account_move_line.items():
            if field_name == 'is_free_goods' or field_name == 'is_overlanded_goods':
                _logger.info("trading_free_goods modules is installed.")
                trading_free_goods = True
                break
        
        return trading_free_goods
    
    @api.onchange('m_price_list')
    def _onchange_product_id_account_invoice_pricelist(self):
        price_list = self.env['product.pricelist'].search([('id', '=', self.move_id.price_list_id.id)])
        checker = self._check_free_goods_module()
        
        for lines in self:
            amount_tax = 0
            amount_untaxed = 0
            
            if price_list:
                if not lines.name == 'Free Good(s)':
                    prod_price_list = self.env['product.pricelist.item'].search([('pricelist_id', '=', price_list.id),
                                                                                ('product_tmpl_id', '=', lines.product_id.product_tmpl_id.id)], limit=1)
                    lines.price_unit = prod_price_list.fixed_price * lines.product_uom_id.factor_inv
                    lines.price_subtotal = (lines.price_unit * lines.quantity) 
                    lines.price_subtotal = (lines.price_unit * lines.quantity) 
                    lines.price_subtotal = (lines.price_unit * lines.quantity) 
                    if lines.tax_ids:
                        lines.price_subtotal = lines.price_subtotal / \
                            ((lines.tax_ids.amount/100)+1)
                        amount_untaxed += lines.price_subtotal
                        amount_tax += lines.price_subtotal * \
                            (lines.tax_ids.amount/100)
                            
                else:
                    lines.price_unit = 0
                    lines.price_subtotal = 0

            else:
                lines.price_unit = 0
                lines.price_subtotal = 0
                
            lines.update(lines._get_price_total_and_subtotal())
            lines.update(lines._get_fields_onchange_subtotal())