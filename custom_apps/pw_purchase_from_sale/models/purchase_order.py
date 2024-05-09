# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    purchase_count = fields.Integer(compute='_compute_purchase_count', string='Purchase')

    def _compute_purchase_count(self):
        for sale in self:
            sale.purchase_count = self.env['purchase.order'].search_count([('pw_sale_id', '=', sale.id)])

    def open_purchase_order(self):
        return {
            'name': ('Purchase Order'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'purchase.order',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'domain': [('pw_sale_id', '=', self.id)],
        }


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    pw_sale_id = fields.Many2one('sale.order', readonly=True)
