from odoo import _, api, models, fields
from odoo.exceptions import ValidationError

class AccountJournal(models.Model):
    _inherit = 'account.journal'
    
    # type = fields.Selection(selection_add=[('debit_credit', "Debit/Credit Card"),
    #                                        ('check', 'Check'),
    #                                        ('others', "Others"),
    #                                        ('deposit', "Direct Deposit/Wire Transfer")], ondelete='cascade')
    
    # type = fields.Selection([
    #         ('sale', 'Sales'),
    #         ('purchase', 'Purchase'),
    #         ('cash', 'Cash'),
    #         ('bank', 'Bank'),
    #         ('general', 'Miscellaneous'),
    #         ('debit_credit', "Debit/Credit Card"),
    #                                        ('check', 'Check'),
    #                                        ('others', "Others"),
    #                                        ('deposit', "Direct Deposit/Wire Transfer")
    #     ])