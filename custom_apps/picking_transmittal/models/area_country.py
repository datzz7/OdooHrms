# -*- coding: utf-8 -*-
#################################################################################
# Author      : Acespritech Solutions Pvt. Ltd. (<www.acespritech.com>)
# Copyright(c): 2012-Present Acespritech Solutions Pvt. Ltd.
# All Rights Reserved.
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#################################################################################

from odoo import fields, models, api


class SalesArea(models.Model):
    _name = "sales.area"
    _description = "Sales Area"
    _rec_name = 'country_id'

    country_id = fields.Many2one(comodel_name='res.country.province', string="Area", required=True,)
    salesman_id = fields.Many2one(comodel_name='res.users', string='Salesman',
                                  default=lambda self: self.env.user)
    encoder_id = fields.Many2one(comodel_name='res.users', string='Encoder',
                                 default=lambda self: self.env.user)

