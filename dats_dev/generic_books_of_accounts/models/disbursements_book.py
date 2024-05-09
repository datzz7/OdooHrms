from odoo import models, fields, api


class DisbursementsBook(models.Model):
    _name = 'briq.disbursements.book'
    
    date = fields.Date(default=fields.date.today())
    payment_date = fields.Date()
    partner_id = fields.Many2one(comodel_name='res.partner', string="Customer")
    or_number = fields.Char()
    invoice_no = fields.Char()
    amount = fields.Float()
    wtax_amount = fields.Float()
    account_id = fields.Many2one(comodel_name='account.account', string="Account")
    tin_no = fields.Char()
    journal_id = fields.Many2one(comodel_name='account.journal', string="Journal")
    payment_id = fields.Many2one(comodel_name='account.payment')
    currency_id = fields.Many2one(comodel_name='res.currency')
