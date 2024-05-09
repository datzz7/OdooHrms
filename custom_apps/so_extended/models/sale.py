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

from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    order_type = fields.Selection(string='Order Type',
                                  selection=[('Cash', 'Cash'), ('Charge', 'Charge'),
                                             ('TRA', 'TRA')], default='Cash')
    country_id = fields.Many2one('sales.area', string="Area")
    vat = fields.Char(string='Vat', related='partner_id.vat', readonly=True)


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
