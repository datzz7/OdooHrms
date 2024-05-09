# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move.line'
    
    variant_model_id = fields.Many2one(comodel_name='product.variant.model', string="Model",)
    variant_warranty_id = fields.Many2one(comodel_name='product.variant.warranty', string="Warranty",)
    
    # @api.model
    # def create(self, vals):
    #     res = super(AccountMove,self).create(vals)
    #     if res.move_id.move_type == 'out_invoice':
    #         convert_to_string = [lines[2] for lines in vals['sale_line_ids']]
    #         convert_to_float = str(convert_to_string)
    #         # sale_lines = ([int(str(lines[2])) for lines in vals['sale_line_ids']])
    #         raise UserWarning(int(convert_to_string))
    #         sale_line_id = self.env['sale.order.line'].search([('id','=',sale_lines)])
    #         # vals['account_id'] = 20
    #         raise UserWarning(sale_line_id)
    #     # raise UserWarning(vals['sale_line_ids'])
        
    #     return res