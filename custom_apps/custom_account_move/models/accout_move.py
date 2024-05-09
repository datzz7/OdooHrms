from odoo import api,fields,models,tools


class AccountMoveInherit(models.Model):
    _inherit="account.move"

    dr_ref = fields.Char(string = "DR Reference")