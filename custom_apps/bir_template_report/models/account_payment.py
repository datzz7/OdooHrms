from odoo import models,fields,api,tools

class AccountPaymentInheritance(models.Model):
    _inherit= "account.payment"


    def convert_amount_to_word(self,value):
        val = str(self.currency_id.amount_to_text(value))

        return val