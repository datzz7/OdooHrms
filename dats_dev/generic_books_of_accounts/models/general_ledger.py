# -*- coding: utf-8 -*-

from odoo import models, fields, api


class GeneralLedger(models.Model):
    _name = 'briq.general.ledger'
    _rec_name = 'move_id'
    
    name = fields.Char()    
    move_id = fields.Many2one(comodel_name='account.move', string="Trx #")
    partner_id = fields.Many2one(comodel_name='res.partner', string="Customer")
    date = fields.Date(default=fields.date.today())
    account_id = fields.Many2one(comodel_name='account.account', string="Account")
    debit = fields.Float()
    credit = fields.Float()
    total_amount = fields.Monetary(string="Amount")
    journal_id = fields.Many2one(comodel_name='account.journal', string="Journal")
    currency_id = fields.Many2one(comodel_name='res.currency')
    
    
