# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
    line_no = fields.Integer(compute='_get_line_numbers', string='Serial Number',readonly=False, default=False)
    
    @api.depends('product_id')
    def _get_line_numbers(self):
        line_num = 1
        line_bug = 0
        
        if not self.ids:
            for line_rec in self.order_id.order_line:
                    line_rec.line_no = line_bug
                    line_bug += 1
                    
        elif self.ids:
            first_line_rec = self.browse(self.ids[0])

            for line_rec in first_line_rec.order_id.order_line:
                line_rec.line_no = line_num
                line_num += 1