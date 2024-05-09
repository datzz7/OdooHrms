# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SalesBook(models.Model):
    _name = 'briq.sales.book'
    _description = 'Sales Book'
    _rec_name = 'invoice_id'

    name = fields.Char()
    invoice_date = fields.Date()
    posting_date = fields.Date()
    invoice_id = fields.Many2one(comodel_name='account.move', string="Customer Invoice")
    partner_id = fields.Many2one(comodel_name='res.partner', string="Customer")
    tin_no = fields.Char(string="TIN")
    creditable_wtax = fields.Float(string="Creditable WTAX")
    output_tax = fields.Float(string="Output")
    acc_receivable = fields.Float(string="Accounts Receivable")
    sales_vat = fields.Float(string="Sales Vatable")
    sales_gov = fields.Float(string="Sales to Government")
    sales_zero = fields.Float(string="Sales-Zero Rated")
    sales_vat_exempt = fields.Float(string="Sales-VAT Exempt")
    account_id = fields.Many2one(comodel_name='account.account', string="Account")