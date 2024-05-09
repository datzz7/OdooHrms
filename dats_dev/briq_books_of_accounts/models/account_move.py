# -*- coding: utf-8 -*-

from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = 'account.move'
    
    
    def action_post(self):
        res = super(AccountMove, self).action_post()
        for rec in self:
            if rec.move_type == 'out_invoice':
                rec._create_sales_book()
        return res
    
    def _create_sales_book(self):
        zrated = 0.00
        govt = 0.00
        sales_vatable = 0.00
        sales_vat_exempt = 0.00
        partner_tin_no = self.partner_id.vat
        cash_amount = self.amount_total if self.amount_total > 0 else None
        
        for lines in self.line_ids:
            if 'Vat Exempt' in lines.account_id.name:
                sales_vat_exempt += lines.price_subtotal
                raise UserWarning(lines.price_subtotal)
            if 'Government' in lines.account_id.name:
                govt += lines.price_subtotal
            if 'Vatable' in lines.account_id.name:
                sales_vatable += lines.price_subtotal
            if 'Zero Rated' in lines.account_id.name:
                zrated += lines.price_subtotal
                
            return {
                'invoice_id': self.id,
                'name': self.name,
                'date_invoice': self.date_invoice,
                'posting_date': fields.date.today(),
                'partner_id': self.partner_id.id,
                'tin': partner_tin_no,
                'acc_receivable':cash_amount - self.wt_rate, 
                'account_id': self.account_id.id,
                'output_tax': self.amount_tax,
                'sales_vat':sales_vatable,
                'creditable_wtax': self.wt_rate, 
                'sales_gov': govt,
                'sales_zero': zrated,
                'sales_vat_exempt': sales_vat_exempt,
            }
        
        


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'
    
    wtax_id = fields.Many2one(comodel_name='account.tax', string="EWT")
    wtax_amount = fields.Float(string="WT Amount", compute='_compute_wtax_amount')
    
    @api.depends('wtax_id', 'account_id')
    def _compute_wtax_amount(self):
        wt_rate = 0
        for line in self:
            tax_val = line.wt_tax_id.amount
            vat = (tax_val / 100)
            if line.price_subtotal:
                wt_rate = (line.price_subtotal * vat)
            line.wtax_amount = wt_rate