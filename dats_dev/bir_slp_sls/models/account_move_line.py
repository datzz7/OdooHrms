# -*- coding: utf-8 -*-

from odoo import models, fields, api

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'
    
    wtax_id = fields.Many2one(comodel_name='account.tax', domain=[('is_withholding_tax', '=', True)])
    wtax_amount = fields.Float(string="Wtax amount", compute='_compute_wtax_amount')
    aml_wtax_prod_id = fields.Many2one(comodel_name='account.move.line')
    
    @api.depends('wtax_id', 'price_unit', 'tax_ids', 'quantity')
    def _compute_wtax_amount(self):
        wtax_amount = 0
        for rec in self:
            if rec.wtax_id:
                tax_val = rec.wtax_id.amount
                vat = (tax_val / 100)
                if rec.tax_ids:
                    wtax_amount = (((rec.price_unit*rec.quantity)/1.12) * vat)
                else:
                    wtax_amount = ((rec.price_unit*rec.quantity) * vat)
            
                rec.wtax_amount = abs(wtax_amount)
            else:
                rec.wtax_amount = 0
            
    
    @api.onchange('product_id','wtax_id','price_unit', 'quantity')
    def _onchange_wtax_id(self):
        for rec in self:
            if rec.move_id.move_type in ('in_invoice', 'out_invoice'):
                journal_entry = self.env['account.move.line'].search([('move_id', '=', rec.move_id._origin.id), ('id','!=', rec._origin.id)])
                if journal_entry:
                    for entry in journal_entry.with_context(check_move_validity=False, force_delete=True):
                        if entry.name:
                            wtax_code = entry.name.split(" ")[0]
                            if wtax_code == rec.product_id.default_code:
                                entry.update({'price_unit': -abs(round(rec.wtax_amount, 2)),
                                            'credit': round(rec.wtax_amount, 2)})
                                if not rec.wtax_id:
                                    entry.update({'price_unit': 0,
                                                'credit': 0})
                        