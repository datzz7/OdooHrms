from odoo import models,api,fields,tools
from odoo.exceptions import UserError,ValidationError

class AccountMoveInherit(models.Model):
    _inherit = "account.move"

    def convert_amount_to_word(self,value):
        val = str(self.currency_id.amount_to_text(value))

        return val
    
    def return_invoice_payments(self):
        lines = self.env['account.move.line'].search([('move_id','=',self.id),('account_id.user_type_id.type','in',('receivable','payable'))])
        partial_recon = False
        payments = []
        if lines:
            if lines.account_id.user_type_id.type == 'receivable':
                partial_recon = self.env['account.partial.reconcile'].search([('debit_move_id','=',lines.id)])
                for i in partial_recon:
                    inv = self.env['account.move.line'].search([('id','=',i.credit_move_id.id)])
                    payment = inv.payment_id
                    if inv.pdc_id:
                        payments.append({
                                'payment_date': inv.pdc_id.payment_date,
                                'ref': inv.pdc_id.memo,
                                'journal': inv.pdc_id.journal_id.name,
                                'check_no':inv.pdc_id.reference,
                                'check_date':inv.pdc_id.payment_date,
                                'amount':i.amount
                        })
                    else:
                        payments.append({
                                'payment_date': payment.date,
                                'ref': payment.name,
                                'journal': payment.move_id.name,
                                'check_no':inv.pdc_id.reference,
                                'check_date':inv.pdc_id.payment_date,
                                'amount':i.amount
                            })
                    #    raise UserError(str(payments))
            else:
                partial_recon = self.env['account.partial.reconcile'].search([('credit_move_id','=',lines.id)])
                for i in partial_recon:
                    inv = self.env['account.move.line'].search([('id','=',i.debit_move_id.id)])
                    payment = inv.payment_id
                    if inv.pdc_id:
                        payments.append({
                                'payment_date': inv.pdc_id.payment_date,
                                'ref': inv.pdc_id.memo,
                                'journal': inv.pdc_id.journal_id.name,
                                'check_no':inv.pdc_id.reference,
                                'check_date':inv.pdc_id.payment_date,
                                'amount':i.amount
                        })
                    else:
                        payments.append({
                                'payment_date': payment.date,
                                'ref': payment.name,
                                'journal': payment.move_id.name,
                                'check_no':inv.pdc_id.reference,
                                'check_date':inv.pdc_id.payment_date,
                                'amount':i.amount
                            })

        

        return payments
        