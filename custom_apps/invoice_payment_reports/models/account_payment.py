# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.addons import decimal_precision as dp

class AccountPayment(models.Model):
    _inherit = 'account.payment'
    
    check_amount = fields.Float(string='Check Amount', digits=dp.get_precision('Product Price'),compute="get_check_amount")
    check_amount_in_word = fields.Char(string="Check Amount(in words)", compute="get_check_amount_in_word")
    
    @api.depends('check_amount')
    def get_check_amount_in_word(self):
        amount_word = self.currency_id.amount_to_text(self.check_amount)
        self.check_amount_in_word =amount_word
        
    @api.depends('amount','tax_amount')
    def get_check_amount(self):
        for rec in self:
            amount = rec.amount
            tax_amount = rec.tax_amount        
            check_amount =(amount - float(tax_amount))
            rec.check_amount = check_amount