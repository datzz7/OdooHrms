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

from datetime import datetime

from odoo import api, fields, models


class PickingTransmittal(models.Model):
    _name = "picking.transmittal"
    _description = "Picking Transmittal"
    _order = 'name desc'

    name = fields.Char(string="Name", required=True, readonly=True, copy=False, default='New')
    area_country_id = fields.Many2one(comodel_name='sales.area', string="Area", required=True)
    trans_salesman_id = fields.Many2one(comodel_name='res.users', string='Salesman')
    transmittal_to = fields.Many2one(comodel_name='res.users', string='Transmittal To')
    prepared_by = fields.Many2one(comodel_name='res.users', string='Prepared By', required=True,
                                  default=lambda self: self.env.uid)
    date_create = fields.Datetime(string='Date/Time Created', required=True, default=datetime.now())
    transmitted_date = fields.Datetime(string='Date/Time Transmitted', readonly=True)
    received_date = fields.Datetime(string='Date/Time Received', readonly=True)
    state = fields.Selection(string='Status', required=True,
                             selection=[('draft', 'Draft'), ('sent', 'Sent'),
                                        ('received', 'Received'),
                                        ('returned', 'Returned'), ('cancelled', 'Cancelled')],
                             default='draft')
    picking_ids = fields.Many2many(comodel_name='stock.picking', string='Picking Lines',
                                   relation='picking_transmittal_stock_picking_rel',
                                   domain="[('area_country_id','!=',False)]")

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            name = self.env["ir.sequence"].next_by_code("picking.transmittal")
            vals["name"] = name
        if not vals.get('date_create'):
            vals['date_create'] = fields.Datetime.now()
        transmittal = super(PickingTransmittal, self).create(vals)
        if transmittal.picking_ids:
            transmittal.picking_ids.write({'transmittal_id': transmittal.id})
        transmittal.write({'trans_salesman_id': transmittal.area_country_id.salesman_id.id,
                           'transmittal_to': transmittal.area_country_id.encoder_id.id,
                           })
        return transmittal

    @api.onchange('area_country_id')
    def _onchange_area_country_id(self):
        self.trans_salesman_id = self.area_country_id.salesman_id
        self.transmittal_to = self.area_country_id.encoder_id

    def action_transmittal(self):
        state = self._context.get('transmittal_state')
        vals = {'state': state}
        if state == 'sent':
            vals['transmitted_date'] = fields.Datetime.now()
        elif state == 'received':
            vals['received_date'] = fields.Datetime.now()
        self.write(vals)

    def print_picking_transmittal(self):
        return self.env.ref('picking_transmittal.action_picking_transmittal_report').report_action(
            self)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    salesman_id = fields.Many2one('res.users', related="country_id.salesman_id",  string="Salesman")

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4
