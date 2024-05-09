# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'
    
    principal_discount = fields.Char(string="Principal Disc.")
    company_discount = fields.Char('Company Disc.')
    
    
    @api.model
    def create(self, vals):
        res = super(AccountMoveLine, self).create(vals)
        for rec in res:
            if rec.sale_line_ids:
                sale_line_id = rec.sale_line_ids
                res.principal_discount = sale_line_id.principal_discount
                res.company_discount = sale_line_id.company_discount
            
        move_id = self.env['account.move'].search([('id', '=', res.move_id.id)])
        p_discount = 0
        c_discount = 0
        
        for rec in move_id.invoice_line_ids:
            p_discount += rec.principal_discount_amount
            c_discount += rec.company_discount_amount

        if res['name'] == 'Principal Discount':
            res['price_unit'] = -p_discount

        if res['name'] == 'Company Discount':
            res['price_unit'] = -c_discount
        return res

    @api.depends('quantity', 'price_unit', 'principal_discount', 'company_discount')
    @api.onchange('principal_discount', 'company_discount')
    def onchange_multi_discount(self):

        def get_discount(percentage, amount):
            new_amount = (percentage * amount)/100
            return (amount - new_amount)

        for rec in self:
            if rec.move_id.move_type == 'out_invoice':
                # if rec.move_id.sale_id.principal_discount_amount or rec.move_id.sale_id.company_discount_amount:
                #     for sales in rec.move_id.sale_id.order_line:
                #         if rec.product_id.id == sales.product_id.id:
                #             if sales.principal_discount:
                #                 rec.principal_discount = sales.principal_discount
                #             if sales.multi_discount:
                #                 rec.multi_discount = sales.multi_discount

                if rec.principal_discount:
                    discount = 0
                    discounted_price = []
                    company_discount_amount = 0
                    amount = 100
                    principal_discounts = rec.principal_discount.split("+")
                    for princ_disc in principal_discounts:
                        amount = get_discount(float(princ_disc), amount)
                    discount = 100 - amount
                    rec.principal_discount_amount = (
                        rec.price_unit * rec.quantity) * (discount/100)

                    if rec.company_discount:
                        price_total = (rec.price_total) - \
                            (rec.price_total * (discount/100))
                        splited_discounts = rec.company_discount.split("+")
                        for disocunt in splited_discounts:
                            discounted_price_total = (
                                (price_total) * (float(disocunt)/100))
                            price_total = price_total - discounted_price_total
                            discounted_price.append(
                                round(discounted_price_total, 2))

                        for disc in discounted_price:
                            company_discount_amount += disc
                        rec.company_discount_amount = company_discount_amount
                    else:
                        rec.company_discount_amount = 0

                elif not rec.principal_discount:
                    rec.principal_discount_amount = 0
                    discounted_price = []
                    company_discount_amount = 0
                    if rec.company_discount:
                        price_total = rec.price_total
                        splited_discounts = rec.company_discount.split("+")
                        for disocunt in splited_discounts:
                            discounted_price_total = (
                                (price_total) * (float(disocunt)/100))
                            price_total = price_total - discounted_price_total
                            discounted_price.append(
                                round(discounted_price_total, 2))

                        for disc in discounted_price:
                            company_discount_amount += disc
                        rec.company_discount_amount = company_discount_amount

                    else:
                        rec.company_discount_amount = 0
                        rec.principal_discount_amount = 0
                        rec.discount = 0

                else:
                    rec.company_discount_amount = 0
                    rec.principal_discount_amount = 0
                    rec.discount = 0

    principal_discount_amount = fields.Float(
        string='Principal Total Discount', compute='onchange_multi_discount', store=True)
    company_discount_amount = fields.Float(
        string='Company Total Discount', compute='onchange_multi_discount', store=True)
    
    