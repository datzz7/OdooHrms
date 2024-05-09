# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockMovLine(models.Model):
    _inherit = 'stock.move.line'
    
    lot_id = fields.Many2one(
        'stock.production.lot', 'Lot/Serial Number',
        domain="[('product_id', '=', product_id), ('company_id', '=', company_id),('stock_prod_qty', '!=', 0)]", check_company=True)
    
    
class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'
    
    
    stock_prod_qty = fields.Float(related='product_qty', store=True)
    status_lot = fields.Char(compute='_get_lot_state')
    lot_ref = fields.Char(compute='_get_reference', string="Reference")
    
    @api.depends('stock_prod_qty')
    def _get_lot_state(self):
        for rec in self:
            status = ''
            if rec.stock_prod_qty > 0:
                status = 'Available'
            else:
                status= 'Not Available'
                
            rec.status_lot = status
        
    @api.depends('quant_ids')
    def _get_reference(self):
        for rec in self:
            ref = ''
            stock_move_line = self.env['stock.move.line'].search([('lot_id', '=', rec.id),('picking_id.picking_type_id.code','=','outgoing'),('picking_id.state','=','done')
                                                                  ],order='create_date desc')
            for lines in stock_move_line:
                ref = lines.reference
                break
            
            rec.lot_ref = ref
                