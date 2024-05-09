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

from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    area_country_id = fields.Many2one(comodel_name='sales.area', string="Country")
    dispatch_id = fields.Many2one(comodel_name='invoice.dispatch', string="Dispatch No.")

    @api.model
    def create(self, vals):
        move = super(AccountMove, self).create(vals)
        picking_id = move.picking_id
        move.write({
                       'area_country_id': picking_id.area_country_id.id if picking_id.area_country_id else False})
        return move

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
