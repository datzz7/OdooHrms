from odoo import models, fields, api, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    analytic_accounts = fields.Many2one('account.analytic.account', string="Analytic")
    analytic_tag_ids = fields.Many2many('account.analytic.tag', string="Analytic Tags")
    material_request_id = fields.Many2one(comodel_name='material.request', store=True)
    


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
    @api.onchange('product_id')
    def preset_analytics(self):
        for rec in self:
            if rec.order_id:
                rec.analytic_account_id = rec.order_id.analytic_accounts.id
                rec.analytic_tag_ids = [(6,0,rec.order_id.analytic_tag_ids.ids)]
        
        