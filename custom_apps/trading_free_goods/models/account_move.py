# -*- coding: utf-8 -*-

from odoo import models, api, fields, _
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = 'account.move'
    
    
    @api.model_create_multi
    def create(self, vals_list):
        res = super(AccountMove, self).create(vals_list)
        if any('state' in vals and vals.get('state') == 'posted' for vals in vals_list):
            raise UserError(_(
                'You cannot create a move already in the posted state. Please create a draft move and post it after.'))
        move = []
        overlanded_goods_data = []
        picking_id = res.picking_id
        sequence = 50000
        overlanded_sequence = 60000
        
        if picking_id.with_free_goods == True:
            move.append((0, 0, {
                            'display_type': 'line_section',
                            'name': 'Free Good(s)',
                            'quantity': 0,
                            'discount': 0,
                            'credit': 0,
                            'price_unit': 0,
                            'account_id': None,
                            'sequence': sequence
                        }))
            for each in picking_id.free_goods_line_ids:
                if len(each) > 0: 
                    move.append((0,0,{
                        'product_id': each.product_id.id,
                        'name': 'Free Good(s)',
                        'quantity': each.quantity,
                        'product_uom_id': each.uom_id.id,
                        'sequence': sequence,
                        'price_unit': 0,
                        'is_free_goods': True
                    }))
                    sequence+=1
            res.write({'invoice_line_ids': move,
                        'move_type': 'out_invoice' if picking_id.picking_type_id.code == 'outgoing' else  'in_invoice',
                    })
            
        if picking_id.with_overlanded_goods == True:
            overlanded_goods_data.append((0, 0, {
                    'display_type': 'line_section',
                    'name': 'Overlanded Good(s)',
                    'quantity': 0,
                    'discount': 0,
                    'credit': 0,
                    'price_unit': 0,
                    'account_id': None,
                    'sequence': overlanded_sequence
                }))
            for each in picking_id.overlanded_goods_line_ids:
                if len(each) > 0: 
                    overlanded_goods_data.append((0,0,{
                        'product_id': each.product_id.id,
                        'name': 'Free Good(s)',
                        'quantity': each.quantity,
                        'product_uom_id': each.uom_id.id,
                        'price_unit': each.product_id.standard_price,
                        'sequence': overlanded_sequence,
                        'is_overlanded_goods': True
                    }))
                    overlanded_sequence+=1
            res.write({'invoice_line_ids': overlanded_goods_data,
                        'move_type': 'out_invoice' if picking_id.picking_type_id.code == 'outgoing' else  'in_invoice'
                    })
        
        return res
    
class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'
    
    is_free_goods = fields.Boolean()
    is_overlanded_goods = fields.Boolean()