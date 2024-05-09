# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    # last_name = fields.Char()
    # first_name = fields.Char()
    # middle_name = fields.Char()
    # full_name = fields.Char(compute='_compute_partner_full_name')
    
    # @api.depends('first_name', 'last_name', 'middle_name', 'company_type')
    # def _compute_partner_full_name(self):
    #     self.fullname = (self.last_name or '')+' '+(self.first_name or '')+' '+(self.middle_name or '')
        
        