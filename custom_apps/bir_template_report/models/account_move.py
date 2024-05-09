from odoo import models,api,fields,tools

class AccountMoveInherit(models.Model):
    _inherit = "account.move"

    def convert_amount_to_word(self,value):
        val = str(self.currency_id.amount_to_text(value))

        return val