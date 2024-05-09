# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
     
    @api.depends('order_line.price_unit','order_line.principal_discount_amount','order_line.company_discount_amount','order_line.price_subtotal')
    def _get_principal_company_discount(self):
        self.principal_discount_amount = 0
        self.company_discount_amount = 0
        principal_discount_amount = 0
        company_discount_amount = 0
        for rec in self.order_line:
            principal_discount_amount += rec.principal_discount_amount if rec.principal_discount_amount else 0
            company_discount_amount += rec.company_discount_amount if rec.company_discount_amount else 0
        self.principal_discount_amount = principal_discount_amount 
        self.company_discount_amount = company_discount_amount 
        
        self.discount_changes()
        
    principal_discount_amount = fields.Float(string='Principal Total Discount',compute='_get_principal_company_discount')
    company_discount_amount = fields.Float(string='Company Total Discount',compute='_get_principal_company_discount')
    
    @api.model
    def create(self,vals):
        res = super(SaleOrder, self).create(vals)
        discounts = []
        principal_amount_discount = vals.get('principal_discount_amount')
        company_amount_discount = vals.get('company_discount_amount')
        discounts_id = self.env['product.product'].search([('name','ilike','Discount')])
        
        for rec in discounts_id:
            if rec.name in 'Principal Discount' and principal_amount_discount:
                discounts.append((0,0,{
                    'product_id': rec.id,
                    'product_uom_qty': 1,
                    'price_unit': principal_amount_discount * -1,
                    'sequence': 500000,
                }))
                
            if rec.name in 'Company Discount' and company_amount_discount:
                discounts.append((0,0,{
                    'product_id': rec.id,
                    'product_uom_qty': 1,
                    'price_unit': company_amount_discount * -1,
                    'sequence': 500001,
                }))
                
        if discounts:
            res.write({'order_line':discounts})
        
        return res
    
    @api.depends('principal_discount_amount','company_discount_amount')
    def discount_changes(self):
        for rec in self.order_line:
            if rec.name == 'Principal Discount':
                rec.update({'price_unit': -(self.principal_discount_amount)})
            
            if rec.name == 'Company Discount':
                rec.update({'price_unit': -(self.company_discount_amount)})
        # self.discount_amount = self.principal_discount_amount + self.company_discount_amount
        return True