# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    principal_discount = fields.Char(string="Principal Disc.")
    company_discount = fields.Char('Company Disc.')
    
    
    @api.depends('price_unit','principal_discount','principal_discount')
    @api.onchange('principal_discount','company_discount')
    def _onchange_company_discount(self):
        def get_discount(percentage,amount):
            new_amount = (percentage * amount)/100
            return (amount - new_amount)
        
        for rec in self:
            if rec.principal_discount:
                discount = 0
                discounted_price = []
                company_discount_amount = 0
                amount = 100
                principal_discounts = rec.principal_discount.split("+")
                for princ_disc in principal_discounts:
                    amount = get_discount(float(princ_disc),amount)
                discount = 100 - amount
                rec.principal_discount_amount = (rec.price_unit * rec.product_uom_qty) * (discount/100)
                
                if rec.company_discount:
                    price_total = (rec.price_total) - (rec.price_total * (discount/100))
                    splited_discounts = rec.company_discount.split("+")
                    for disocunt in splited_discounts:
                        discounted_price_total = ((price_total) *(float(disocunt)/100))
                        price_total = price_total - discounted_price_total
                        discounted_price.append(round(discounted_price_total,2))
                    
                    for disc in discounted_price:
                        company_discount_amount += disc 
                    rec.company_discount_amount = company_discount_amount
                else:
                    rec.company_discount_amount = 0
                    
            elif not rec.principal_discount:
                discounted_price = []
                company_discount_amount = 0
                if rec.company_discount:
                    splited_discounts = rec.company_discount.split("+")
                    price_total = rec.price_total
                    for disocunt in splited_discounts:
                        discounted_price_total = ((price_total) *(float(disocunt)/100))
                        price_total = price_total - discounted_price_total
                        discounted_price.append(round(discounted_price_total,2))
                    
                    for disc in discounted_price:
                        company_discount_amount += disc 
                    rec.company_discount_amount = company_discount_amount

                    rec.principal_discount_amount = 0
                else:
                    rec.company_discount_amount = 0
                    rec.principal_discount_amount = 0
                    rec.discount = 0
                    
            else:
                rec.company_discount_amount = 0
                rec.principal_discount_amount = 0
                rec.discount = 0
            
    principal_discount_amount = fields.Float(string='Principal Total Discount',compute='_onchange_company_discount')
    company_discount_amount = fields.Float(string='Company Total Discount',compute='_onchange_company_discount')
    

    # check if discount > 0: raise error if user is trying to delete discount lines
    def unlink(self):
        if self.order_id.principal_discount_amount > 0 or self.order_id.company_discount_amount > 0:
            if self.name in ['Principal Discount', 'Company Discount']:
                raise UserError("You cannot delete these lines if there are discounted items.")
        
        return models.Model.unlink(self)