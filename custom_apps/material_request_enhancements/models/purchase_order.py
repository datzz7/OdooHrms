from odoo import models, fields, api, _
from odoo.exceptions import UserError

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    partner_id = fields.Many2one(comodel_name='res.partner',required=False, )
    material_request_id = fields.Many2one(comodel_name='material.request',store=True)
    account_analytic_id = fields.Many2one('account.analytic.account', string="Analytic Account")
    analytic_tag_ids = fields.Many2many(comodel_name='account.analytic.tag', relation='purchase_analytic_rel', ) 
    
    def _prepare_picking(self):
        res = super(PurchaseOrder, self)._prepare_picking()
        res.update({'analytic_accounts': self.account_analytic_id.id,
                    'analytic_tag_ids': [(6, 0, self.analytic_tag_ids.ids)]})
        return res
        
    @api.onchange('account_analytic_id', 'analytic_tag_ids')
    def _onchange_analytic_accounts(self):
        for rec in self.order_line:
            rec.update({'account_analytic_id': self.account_analytic_id.id,
                        'analytic_tag_ids': [(6, 0, self.analytic_tag_ids.ids)]})

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'
    
    def _prepare_stock_move_vals(self, picking, price_unit, product_uom_qty, product_uom):
        res = super(PurchaseOrderLine, self)._prepare_stock_move_vals(picking, price_unit, product_uom_qty, product_uom)
        res.update({'analytic_account_id': self.account_analytic_id.id,
                    'analytic_tag_ids': [(6, 0, self.analytic_tag_ids.ids)]})
        return res
    
    