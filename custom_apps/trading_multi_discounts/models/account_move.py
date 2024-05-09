# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = 'account.move'


    @api.depends('invoice_line_ids.price_unit', 'invoice_line_ids.quantity', 'invoice_line_ids.principal_discount_amount', 'invoice_line_ids.company_discount_amount', 'invoice_line_ids.price_subtotal')
    def _get_principal_company_discount(self):
        self.principal_discount_amount = 0
        self.company_discount_amount = 0
        self.total_discounts = 0
        principal_discount_amount = 0
        company_discount_amount = 0
        for rec in self.invoice_line_ids:
            principal_discount_amount += rec.principal_discount_amount if rec.principal_discount_amount else 0
            company_discount_amount += rec.company_discount_amount if rec.company_discount_amount else 0
            rec.recompute_tax_line = True
        self.principal_discount_amount = principal_discount_amount
        self.company_discount_amount = company_discount_amount
        self.total_discounts = principal_discount_amount + company_discount_amount
        for lines in self.invoice_line_ids:
            if lines.name == 'Principal Discount':
                lines.price_unit = -(principal_discount_amount)
            if lines.name == 'Company Discount':
                lines.price_unit = -(company_discount_amount)
        if self.move_type == 'out_invoice':
            self.with_context(check_move_validity=False)._recompute_dynamic_lines(
                recompute_all_taxes=True, recompute_tax_base_amount=True)
            self.principal_discount_amount = principal_discount_amount
            self.company_discount_amount = company_discount_amount
            self.total_discounts = principal_discount_amount + company_discount_amount
        
    principal_discount_amount = fields.Float(
        string='Principal Total Discount', compute='_get_principal_company_discount', Store=True)
    company_discount_amount = fields.Float(
        string='Company Total Discount', compute='_get_principal_company_discount', Store=True)
    total_discounts = fields.Float(
        string='Total Discount', compute='_get_principal_company_discount', Store=True)
    
    @api.depends('discount_is_true')
    @api.onchange('discount_is_true')
    def check_lines_discount(self):
        data = []
        tax = ''
        discount_list = []
        if self.discount_is_true:
            discounts = self.env['product.product'].search(
                [('name', 'ilike', 'Discount')])
            for lines in self.invoice_line_ids:
                tax = lines.tax_ids.ids
                discount_list.append(lines.name)
                
            for disc in discounts:
                if 'Principal Discount' in disc.name and disc.name not in discount_list:
                    data.append((0, 0, {
                        'product_id': disc.id,
                        'account_id': disc.categ_id.property_account_income_categ_id.id,
                        'name': disc.name,
                        'tax_ids': [(6,0,tax)],
                        'currency_id': self.currency_id.id,
                        'quantity': 1,
                    }))

                elif 'Company Discount' in disc.name  and disc.name not in discount_list:
                    data.append((0, 0, {
                        'product_id': disc.id,
                        'account_id': disc.categ_id.property_account_income_categ_id.id,
                        'name': disc.name,
                        'tax_ids': [(6,0,tax)],
                        'currency_id': self.currency_id.id,
                        'quantity': 1,
                    }))

            self.update({'invoice_line_ids': data,
                        'discount_is_true': True})