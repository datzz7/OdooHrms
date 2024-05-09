# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleArea(models.Model):
    _name = 'sales.area'
    _description = "Sales Area"
    _rec_name = 'country_id'

    country_id = fields.Many2one(comodel_name='res.country.province', string="Area", required=True,)
    salesman_id = fields.Many2one(comodel_name='res.users', string='Salesman',
                                  default=lambda self: self.env.user)
    encoder_id = fields.Many2one(comodel_name='res.users', string='Encoder',
                                 default=lambda self: self.env.user)
