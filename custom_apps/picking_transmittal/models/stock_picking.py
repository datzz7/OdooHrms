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

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    area_country_id = fields.Many2one(comodel_name='sales.area', string="Area", related="sale_id.country_id", store=True)
    transmittal_id = fields.Many2one(comodel_name='picking.transmittal', string="Transmittal No")
    vehicle_id = fields.Many2one(comodel_name='fleet.vehicle', string='Vehicle Plate') #Not required
    driver_id = fields.Many2one(comodel_name='res.partner', string='Driver')
    helper_id = fields.Many2one(comodel_name='res.partner', string='Helper')

    salesman_id = fields.Many2one(comodel_name='res.users', related="sale_id.salesman_id", string='Salesman')

    @api.model
    def create(self, vals):
        picking = super(StockPicking, self).create(vals)
        if picking.picking_type_id.code == 'outgoing':
            sale_order = self.env['sale.order'].search([('name', '=', picking.origin)])
            if sale_order:
                picking.write({'user_id': sale_order.user_id.id})
        if picking.vehicle_id:
            picking.write({'driver_id': picking.vehicle_id.driver_id.id,
                            'helper_id': picking.vehicle_id.helper_id.id,
                        })
        return picking

    @api.onchange('vehicle_id')
    def _onchange_vehicle_id(self):
        self.driver_id = self.vehicle_id.driver_id
        self.helper_id = self.vehicle_id.helper_id

    def action_transmittals_create(self):
        area_id = self.mapped('area_country_id')

        if not area_id or any(self.filtered(lambda picking: not picking.area_country_id)):
            raise UserError(_('You can not create transmittal for without country pickings!!'))
        elif len(area_id.ids) > 1:
            raise UserError(_('Please Select those record which have same Country!!'))
        elif any(self.mapped('transmittal_id')):
            raise UserError(
                _('You can not create Transmittal for pickings which have already transmittal!!'))
        else:
            transmittal_rec = self.env['picking.transmittal'].create({'area_country_id': area_id.id,
                                                                      'picking_ids': [(6, 0,
                                                                                       self.ids)]})
            self.write({'transmittal_id': transmittal_rec})

    def _action_generate_backorder_wizard(self, show_transfers=False):
        view = self.env.ref('stock.view_backorder_confirmation')
        return {
            'name': _('Unserved Stock Notification'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'stock.backorder.confirmation',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            'context': dict(self.env.context, default_show_transfers=show_transfers,
                            default_pick_ids=[(4, picking.id) for picking in self]),
        }


class StockPickingType(models.Model):
    _inherit = 'stock.picking.type'

    def _compute_waiting_count(self):
        data = self.env['stock.picking'].read_group([('state', 'in',
                                                      ('confirmed', 'waiting', 'assigned'))] +
                                                    [('state', 'not in', ('done', 'cancel')),
                                                     ('picking_type_id', 'in', self.ids)],
                                                    ['picking_type_id'], ['picking_type_id'])
        count = {
            picking['picking_type_id'][0]: picking['picking_type_id_count']
            for picking in data if picking['picking_type_id']
        }
        for record in self:
            record['count_picking_ready_waiting'] = count.get(record.id, 0)

    count_picking_ready_waiting = fields.Integer(compute='_compute_waiting_count')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4
