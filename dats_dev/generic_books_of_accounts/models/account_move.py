# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'
    
    def action_post(self):
        res = super(AccountMove, self).action_post()
        for rec in self:
            if rec.move_type not in ('out_invoice', 'in_invoice'):
                break
            if rec.move_type == 'out_invoice':
                self.env['briq.sales.book'].create(rec._create_sales_book())
            if rec.move_type == 'in_invoice':
                self.env['briq.purchases.book'].create(rec._create_purchases_book())
            self.env['briq.general.ledger'].create(rec._create_general_ledger())
                
        return res
    
    def _create_sales_book(self):
        for rec in self:
            data = []
            for lines in rec.line_ids:
                if lines.date_maturity:
                    data.append({
                        'move_id': rec.id,
                        'partner_id': rec.partner_id.id,
                        'invoice_date': rec.invoice_date,
                        'tin_no': rec.partner_id.vat,
                        'total_amount': abs(lines.price_total),
                        'debit': abs(lines.price_total),
                        'credit': 0, 
                        'account_id': lines.account_id.id,
                        'date_maturity': lines.date_maturity,
                        'journal_id': rec.journal_id.id,
                        'currency_id': rec.company_currency_id.id
                    })
            return data
        
    def _create_purchases_book(self):
        for rec in self:
            data = []
            for lines in rec.line_ids:
                if lines.date_maturity:
                    data.append({
                        'move_id': rec.id,
                        'partner_id': rec.partner_id.id,
                        'invoice_date': rec.invoice_date,
                        'tin_no': rec.partner_id.vat,
                        'total_amount': abs(lines.price_total),
                        'debit': 0,
                        'credit': abs(lines.price_total),
                        'account_id': lines.account_id.id,
                        'date_maturity': lines.date_maturity,
                        'journal_id': rec.journal_id.id,
                        'currency_id': rec.company_currency_id.id,
                    })
            return data
    
    def _create_general_ledger(self):
        for rec in self:
            data = []
            for lines in rec.line_ids:
                data.append({
                    'name': lines.move_id.name,
                    'move_id': rec.id,
                    'partner_id': lines.partner_id.id,
                    'account_id': lines.account_id.id,
                    'debit': lines.debit,
                    'credit': lines.credit,
                    'total_amount': lines.price_subtotal,
                    'journal_id': rec.journal_id.id,
                    'currency_id': rec.company_currency_id.id,
                })
            return data
    
    def button_draft(self):
        res = super(AccountMove, self).button_draft()
        sales_book_obj = self.env['briq.sales.book'].search([('move_id', '=', self.id)])
        purchase_book_obj = self.env['briq.purchases.book'].search([('move_id', '=', self.id)])
        general_ledger = self.env['briq.general.ledger'].search([('move_id', '=', self.id)])
        if sales_book_obj:
            for sales in sales_book_obj:
                sales.unlink()
        
        if purchase_book_obj:
            for purch in purchase_book_obj:
                purch.unlink()
        
        if general_ledger:
            for gl in general_ledger:
                gl.unlink()
                
        return res