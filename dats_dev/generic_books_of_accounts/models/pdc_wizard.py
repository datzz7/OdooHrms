from odoo import models, api, fields, _


class shPDC(models.Model):
    _inherit = 'pdc.wizard'
    
    def button_register(self):
        res = super(shPDC, self).button_register()
        if self.invoice_id.move_type == 'in_invoice':
            self.env['briq.disbursements.book'].create(self._create_disbursements_book())
        
        if self.invoice_id.move_type == 'out_invoice':
            self.env['briq.receipts.book'].create(self._create_receipts_book())
            
        return res
    
    def _create_disbursements_book(self):
        data = []
        for rec in self:
            data.append({
                'payment_id': rec.id,
                'account_id': rec.journal_id.payment_credit_account_id.id,
                'payment_date': rec.payment_date,
                'invoice_no': rec.name,
                'tin_no': rec.partner_id.vat,
                'amount': rec.payment_amount,
                'partner_id': rec.partner_id.id,
                'or_number': rec.reference,
                'journal_id': rec.journal_id.id
            })
        
        return data
    
    def _create_receipts_book(self):
        data = []
        for rec in self:
            data.append({
                'payment_id': rec.id,
                'account_id': rec.journal_id.payment_debit_account_id.id,
                'payment_date': rec.payment_date,
                'invoice_no': rec.name,
                'tin_no': rec.partner_id.vat,
                'amount': rec.payment_amount,
                'partner_id': rec.partner_id.id,
                'or_number': rec.reference,
                'journal_id': rec.journal_id.id
            })
        
        return data