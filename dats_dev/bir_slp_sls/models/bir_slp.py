# -*- coding: utf-8 -*-

from odoo import models, fields, api


class BIRSLP(models.Model):
    _name = 'bir.slp'
    _description = 'BIR SLP'
    _rec_name = 'account_invoice_id'
    
    account_invoice_id = fields.Many2one(string='Invoice',comodel_name='account.move',)
    purchase_voucher_id = fields.Many2one(comodel_name='account.voucher', string="Purchase Receipt", store=True)
    posting_date = fields.Date(string = "Posting Date",default=fields.Date.today(),)
    vendor_tin = fields.Char(string="Vendor TIN")
    company_name = fields.Many2one(comodel_name='res.partner', string="Company Name")
    last_name = fields.Char(string="lastName")
    first_name = fields.Char(string="firstName")
    middle_name = fields.Char(string="middleName")
    address1 = fields.Char(string="address1")
    address2 = fields.Char(string="address2")
    exempt = fields.Float(string="exempt")
    zero_rated = fields.Float( string="zeroRated")
    services = fields.Float(string="services")
    capital_goods = fields.Float(string="capitalGoods")
    other_capital_goods = fields.Float(string="otherThancapitalGoods",)
    taxable_net_vat = fields.Float(string="taxableNetofVat", )
    vat_rate = fields.Float(string="vatRate")
    input_vat = fields.Float(string="inputVat", )
    total_purchases = fields.Float(string="totalPurchases")    
