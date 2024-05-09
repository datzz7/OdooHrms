# -*- coding: utf-8 -*- 

from odoo import models, fields, api, _

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'
    
    whtax = fields.Boolean('whtax', default=False)
    is_select = fields.Boolean('Select', default=False)