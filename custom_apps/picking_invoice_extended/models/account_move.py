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

    inv_doc_type = fields.Selection(string='Doc Type',
                                    selection=[('Cash', 'Cash'), ('Charge', 'Charge'),
                                            ('TRA', 'TRA')])
    vehicle_id = fields.Many2one(comodel_name='fleet.vehicle', string='Vehicle Plate')
    driver_id = fields.Many2one(comodel_name='res.partner', string='Driver')
    helper_id = fields.Many2one(comodel_name='res.partner', string='Helper')

    @api.model
    def create(self, vals):
        move = super(AccountMove, self).create(vals)
        picking_id = move.picking_id
        move.write({'inv_doc_type': move.sale_id.order_type,
                    'vehicle_id': picking_id.vehicle_id.id,
                    'driver_id': picking_id.driver_id.id if picking_id.driver_id else False,
                    'helper_id': picking_id.helper_id.id if picking_id.helper_id else False,
                    })
        return move

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
