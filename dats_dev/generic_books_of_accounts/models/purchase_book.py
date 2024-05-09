# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PurchasesBook(models.Model):
    _name = 'briq.purchases.book'
    
    name = fields.Char()    
    move_id = fields.Many2one(comodel_name='account.move', string="Trx #")
    partner_id = fields.Many2one(comodel_name='res.partner', string="Customer")
    date = fields.Date(default=fields.date.today())
    account_id = fields.Many2one(comodel_name='account.account', string="Account")
    invoice_date = fields.Date()
    date_maturity = fields.Date()
    tin_no = fields.Char()
    debit = fields.Float()
    credit = fields.Float()
    total_amount = fields.Monetary(string="Amount")
    journal_id = fields.Many2one(comodel_name='account.journal', string="Journal")
    currency_id = fields.Many2one(comodel_name='res.currency')
    
    
    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('books.purchase.sequence')
        res = super(PurchasesBook, self).create(vals)
        return res
    