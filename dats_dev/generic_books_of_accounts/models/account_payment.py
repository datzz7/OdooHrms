from odoo import models, fields, api


class AccountPayment(models.Model):
    _inherit = 'account.payment'
    
    
    def action_post(self):
        res = super(AccountPayment, self).action_post()
        for rec in self:
            if rec.payment_type == 'outbound':
                self.env['briq.disbursements.book'].create(rec._create_disbursements_book())
            if rec.payment_type == 'inbound':
                self.env['briq.receipts.book'].create(rec._create_receipts_book())
        
        return res
    
    
    def _create_disbursements_book(self):
        data = []
        for rec in self:
            data.append({
                'payment_id': rec.id,
                'account_id': rec.destination_account_id.id,
                'payment_date': rec.date,
                'invoice_no': rec.ref,
                'tin_no': rec.partner_id.vat,
                'amount': rec.check_amount,
                'partner_id': rec.partner_id.id,
                'or_number': rec.or_number,
                'journal_id': rec.journal_id.id
            })
        
        return data
    
    def _create_receipts_book(self):
        data = []
        for rec in self:
            data.append({
                'payment_id': rec.id,
                'account_id': rec.destination_account_id.id,
                'payment_date': rec.date,
                'invoice_no': rec.ref,
                'tin_no': rec.partner_id.vat,
                'amount': rec.check_amount,
                'partner_id': rec.partner_id.id,
                'or_number': rec.or_number,
                'journal_id': rec.journal_id.id
            })
        
        return data
    
    def button_draft(self):
        res = super(AccountPayment, self).button_draft()
        disburse_obj = self.env['briq.disbursements.book'].search([('payment_id', '=', rec.id)])
        receipts_obj = self.env['briq.receipts.book'].search([('payment_id', '=', rec.id)])
        
        if disburse_obj:
            for disb in disburse_obj:
                disb.unlink()

        if receipts_obj:
            for recs in receipts_obj:
                recs.unlink()        
                
        return res