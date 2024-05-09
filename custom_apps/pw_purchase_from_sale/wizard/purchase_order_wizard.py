# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class PurchaseOrderWizard(models.TransientModel):
    _name = "purchase.order.wizard"
    _description = 'Purchase Order Wizard'

    partner_id = fields.Many2one('res.partner', string="Vendor", required=True)
    date_order = fields.Datetime(string="Order Date", required=True)
    line_ids = fields.One2many('purchase.order.line.wizard', 'purchase_wizard_id', string="Purchase Id")

    def action_create_order(self):
        active_id = self._context.get('active_id')
        sale_id = self.env['sale.order'].browse(active_id)
        if not self.partner_id:
            raise ValidationError(_('Please set partner!'))
        order_line_list = []
        for line in self.line_ids:
            vals = (0, 0, {
                'name': line.product_id.name,
                'product_id': line.product_id.id or False,
                'product_qty': line.order_qty or False,
                'product_uom': line.product_id.uom_id.id or False,
                'price_unit': line.unit_price,
                'date_planned': self.date_order,
                'product_uom': line.product_uom.id or False,
            })
            order_line_list.append(vals)
        if order_line_list:
            self.env['purchase.order'].sudo().create({
                'partner_id': self.partner_id.id or False,
                'order_line': order_line_list or False,
                'origin': sale_id.name,
                'date_planned': self.date_order,
                'pw_sale_id': sale_id.id,
            })

    @api.model
    def default_get(self, vals):
        purchase_line = []
        res = super(PurchaseOrderWizard, self).default_get(vals)
        active_id = self._context.get('active_id')
        if active_id:
            sale_id = self.env['sale.order'].browse(active_id)
            for sale in sale_id:
                for line in sale.order_line:
                    cons_inv_line = self.env['purchase.order.line.wizard'].create({
                        'product_id': line.product_id.id,
                        'descriptione': line.product_id.name,
                        'order_qty': line.product_uom_qty,
                        'unit_price': line.price_unit,
                        'subtotal': line.price_subtotal,
                        'product_uom': line.product_uom.id,
                    })
                    purchase_line.append(cons_inv_line.id)
                res['partner_id'] = sale_id.partner_id.id
                res['date_order'] = sale_id.date_order
        res['line_ids'] = [[6, 0, purchase_line]]
        return res


class PurchaseOrderLineWizard(models.TransientModel):
    _name = "purchase.order.line.wizard"
    _description = 'Purchase Order Wizard'

    purchase_wizard_id = fields.Many2one('purchase.order.wizard', string="Purchase Id")
    product_id = fields.Many2one('product.product', string="Products")
    descriptione = fields.Char(string="Description")
    order_qty = fields.Float(string="Ordered Qty")
    unit_price = fields.Float(string="Unit Price")
    subtotal = fields.Float(string="Subtotal")
    product_uom = fields.Many2one('uom.uom', string='Unit of Measure')
