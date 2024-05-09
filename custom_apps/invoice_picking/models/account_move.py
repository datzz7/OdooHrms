# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = 'account.move'

    validate_picking = fields.Boolean(default=False, string="With Picking")
    warehouse_id = fields.Many2one(comodel_name='stock.warehouse', string="Warehouse")
    auto_post_picking = fields.Boolean(string="Auto Post Picking")

    
    def action_post(self):
        res = super(AccountMove, self).action_post()
        for rec in self:
            if rec.validate_picking:
                if not rec.warehouse_id:
                    raise UserError(_('Please select warehouse.'))
                
                else:
                    stock_move_lines = []
                    picking_obj = self.env['stock.picking']
                    picking_type_obj = rec.get_operation_type()
                    cust_loc = self.env["stock.location"].search(
                            [("usage", "=", "customer")], limit=1
                        )
                    stock_loc = self.env["stock.location"].search(
                            [("usage", "=", "internal"), ("name", "ilike", "Stock")], limit=1
                        )
                    for line in rec.invoice_line_ids:
                        if line.product_id.type == 'product':
                            stock_move_lines.append((0,0,
                                    {
                                        
                                        "product_id": line.product_id.id,
                                        # "name": line.name,
                                        # "demand_qty": line.quantity,
                                        "qty_done": line.quantity,
                                        "product_uom_id": line.product_uom_id.id,
                                        "location_id": 4,
                                        "location_dest_id": picking_type_obj.default_location_dest_id.id
                                        or cust_loc.id,
                                    },))
                    
                    picking_vals = {
                            "partner_id": rec.partner_id.id,
                            "picking_type_id": picking_type_obj.id,
                            "location_id": 4,
                            "location_dest_id": picking_type_obj.default_location_dest_id.id or cust_loc.id,
                            "move_line_ids_without_package": stock_move_lines,
                            'origin': rec.name,
                            'move_type': 'one',
                            'invoice_id': rec.id,
                            "show_validate": True,
                        }
                    
                    pick = picking_obj.create(picking_vals)
                    if rec.auto_post_picking:
                        pick.action_confirm()
                        if pick:
                            for lines in pick.move_ids_without_package:
                                lines.update({'name': lines.product_id.name})
                            pick.button_validate()
        return res
    
    
    
    def get_operation_type(self):
        for rec in self:
            operation_type = rec.env['stock.picking.type']
            if rec.move_type in ['out_invoice','out_receipt']:
                operation_type = operation_type.search([('warehouse_id','=', rec.warehouse_id.id),
                                                        ('code', '=', 'outgoing')])
            elif rec.move_type in ['in_invoice', 'in_receipt']:
                operation_type = operation_type.search([('warehouse_id','=', rec.warehouse_id.id),
                                                        ('code', '=', 'incoming')])
        return operation_type
    