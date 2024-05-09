from odoo import _, api, models, fields
from odoo.exceptions import ValidationError

class PaymentRegister(models.TransientModel):
    _inherit = 'account.payment.register'
    
    card_bank_provider = fields.Char(string="Card/Bank Provider")
    card_number = fields.Char(string="Card Number")
    remarks = fields.Char(string="Remarks")
    
    check_date = fields.Date(string="Check Date")
    check_bank = fields.Char()
    check_number = fields.Char()
    
    date_deposited = fields.Date(string="Date Deposited/Transferred")
    bank_transferred = fields.Char(string="Bank Transferred/Deposited to")
    
    payment_facility = fields.Char()
    p_date_paid = fields.Date()
    
    payment_type_sel = fields.Selection(selection=[('debit_credit', "Debit/Credit Card"),
                                           ('check', 'Check'),
                                           ('others', "Others"),
                                           ('deposit', "Direct Deposit/Wire Transfer")])
    
    @api.onchange('journal_id')
    def onchange_journal_id_s(self):
        if self.journal_id.name == 'Debit/Credit Card':
            self.payment_type_sel = 'debit_credit'
        elif self.journal_id.name == 'Check':
            self.payment_type_sel = 'check'
        elif self.journal_id.name == 'Others':
            self.payment_type_sel = 'others'
        elif self.journal_id.name == 'Direct Deposit/Wire Transfer':
            self.payment_type_sel = 'deposit'
        else:
            self.payment_type_sel = False
            
            
            