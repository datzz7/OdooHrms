# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.tools import float_is_zero, OrderedSet

class StockMove(models.Model):
    _inherit = 'stock.move'
    
    # Dats: Inherit from core module stock_account
    def _create_in_svl(self, forced_quantity=None):
            """Create a `stock.valuation.layer` from `self`.

            :param forced_quantity: under some circunstances, the quantity to value is different than
                the initial demand of the move (Default value = None)
            """
            svl_vals_list = []
            for move in self:
                move = move.with_company(move.company_id)
                valued_move_lines = move._get_in_move_lines()
                valued_quantity = 0
                for valued_move_line in valued_move_lines:
                    valued_quantity += valued_move_line.product_uom_id._compute_quantity(valued_move_line.qty_done, move.product_id.uom_id)
                unit_cost = abs(move._get_price_unit())  # May be negative (i.e. decrease an out move).
                if move.product_id.cost_method == 'standard':
                    unit_cost = move.product_id.standard_price
                svl_vals = move.product_id._prepare_in_svl_vals(forced_quantity or valued_quantity, unit_cost)
                svl_vals.update(move._prepare_common_svl_vals())
                if forced_quantity:
                    svl_vals['description'] = 'Correction of %s (modification of past move)' % move.picking_id.name or move.name
                svl_vals_list.append(svl_vals)
            return self.env['stock.valuation.layer'].sudo().create(svl_vals_list)
    
    # Dats: Inherit from core module stock_account
    def _create_out_svl(self, forced_quantity=None):
        """Create a `stock.valuation.layer` from `self`.

        :param forced_quantity: under some circunstances, the quantity to value is different than
            the initial demand of the move (Default value = None)
        """
        svl_vals_list = []
        for move in self:
            # Dats Start
            total_cost = 0
            prod_lots = self.env['stock.quant'].search([('lot_id', 'in', (move.lot_ids.ids)), ('company_id','=',1)])
            
            for lots in prod_lots:
                total_cost += lots.cost_price
            # Dats End
                
            move = move.with_company(move.company_id)
            valued_move_lines = move._get_out_move_lines()
            valued_quantity = 0
            for valued_move_line in valued_move_lines:
                valued_quantity += valued_move_line.product_uom_id._compute_quantity(valued_move_line.qty_done, move.product_id.uom_id)
            if float_is_zero(forced_quantity or valued_quantity, precision_rounding=move.product_id.uom_id.rounding):
                continue
            svl_vals = move.product_id._prepare_out_svl_vals(forced_quantity or valued_quantity, move.company_id)
            svl_vals.update(move._prepare_common_svl_vals())
            if forced_quantity:
                svl_vals['description'] = 'Correction of %s (modification of past move)' % move.picking_id.name or move.name
            svl_vals['description'] += svl_vals.pop('rounding_adjustment', '')
            # Dats Start
            if move.product_id.cost_method == 'serialization' and not move.product_id == 'none':
                svl_vals['unit_cost'] = total_cost
                svl_vals['value'] = -abs(total_cost)
            # Dats End
            svl_vals_list.append(svl_vals)
        return self.env['stock.valuation.layer'].sudo().create(svl_vals_list)