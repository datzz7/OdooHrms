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


class InvoiceDispatch(models.Model):
    _name = "invoice.dispatch"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Invoice Dispatch"

    def _get_vehicle(self):
        domain = [('id', '=', -1)]
        vehicle_list = []
        move_ids = self.env['account.move'].search(
            [('vehicle_id', '!=', False), ('state', '=', 'posted')])
        for each in move_ids:
            vehicle_list.append(each.vehicle_id.id)
        if vehicle_list:
            domain = [('id', 'in', vehicle_list)]
            return domain
        return domain

    name = fields.Char(string="Name", required=True, readonly=True, copy=False, store=True,
                       default='New')
    vehicle_id = fields.Many2one(comodel_name='fleet.vehicle', string='Vehicle No',
                                 domain=_get_vehicle)
    driver_id = fields.Many2one(comodel_name='res.partner', string='Driver')
    helper_id = fields.Many2one(comodel_name='res.partner', string='Helper')
    date = fields.Datetime(string='Date', required=True, default=datetime.now())
    dispatch_date = fields.Datetime(string='Dispatch Date')
    note = fields.Text(string='Notes')
    dispatcher_id = fields.Many2one(comodel_name='res.users', string='Dispatcher',
                                    default=lambda self: self.env.user)
    state = fields.Selection(string='Status', required=True,
                             selection=[('draft', 'Draft'), ('ready', 'Ready'),
                                        ('done', 'Done'), ('cancelled', 'Cancelled')],
                             default='draft', tracking=True)
    invoice_ids = fields.Many2many(comodel_name='account.move',
                                   relation='invoice_dispatch_account_move_rel',
                                   string='Invoices')
    company_id = fields.Many2one(comodel_name='res.company', string="Company", store=True,
                                 default=lambda self: self.env.user.company_id.id,
                                 required=True)

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            name = self.env["ir.sequence"].next_by_code("invoice.dispatch")
            vals["name"] = name
        if not vals.get('date'):
            vals['date'] = fields.Datetime.now()
        move_ids = self.env['account.move'].search(
            [('vehicle_id', '=', int(vals.get('vehicle_id'))), ('state', '=', 'posted'),
             ('dispatch_id', '=', False)]).ids
        if move_ids:
            vals['invoice_ids'] = [(6, 0, move_ids)]
        dispatch = super(InvoiceDispatch, self).create(vals)
        dispatch.write({'driver_id': dispatch.vehicle_id.driver_id.id,
                        'helper_id': dispatch.vehicle_id.helper_id.id,
                        })
        if dispatch.invoice_ids:
            dispatch.invoice_ids.write({'dispatch_id': dispatch.id})
        return dispatch

    def write(self, vals):
        res = super(InvoiceDispatch, self).write(vals)
        if vals.get('invoice_ids'):
            self.invoice_ids.write({'dispatch_id': self.id})
            return res
        return res

    @api.onchange('vehicle_id')
    def _onchange_vehicle_id(self):
        if self.vehicle_id:
            self.driver_id = self.vehicle_id.driver_id
            self.helper_id = self.vehicle_id.helper_id
            lst_move_ids = self.env['account.move'].search(
                [('vehicle_id', '=', self.vehicle_id.id), ('state', '=', 'posted'),
                 ('dispatch_id', '=', False)]).ids
            self.invoice_ids = [(6, 0, lst_move_ids)]

    def action_invoice_dispatch(self):
        state = self._context.get('dispatch_state')
        vals = {'state': state}
        if state == 'ready':
            vals['date'] = fields.Datetime.now()
        elif state == 'done':
            vals['dispatch_date'] = fields.Datetime.now()
        self.write(vals)

    def print_invoice_dispatch(self):
        return self.env.ref('invoice_dispatch_fleet.action_invoice_dispatch_report').report_action(
            self)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
