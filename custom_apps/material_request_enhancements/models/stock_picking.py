from odoo import models, fields, api, _
from odoo.exceptions import UserError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    analytic_accounts = fields.Many2one('account.analytic.account', string="Analytic")
    analytic_tag_ids = fields.Many2many('account.analytic.tag', string="Analytic Tags")
    material_request_id = fields.Many2one(comodel_name='material.request')

    @api.model
    def create(self, vals):
        purch_id = self.env['purchase.order'].search([('name', '=', vals.get('origin'))])
        sale_id = self.env['sale.order'].search([('name', '=', vals.get('origin'))])

        # raise UserError(_(purch_id))
        for rec in purch_id:
            if rec:
                vals.update({
                    # 'analytic_accounts': purch_id.analytic_accounts.id,
                             'material_request_id': rec.material_request_id.id})

        for sale in sale_id:
            if sale:
                vals.update({
                    # 'analytic_accounts': sale_id.analytic_accounts.id,
                             'material_request_id': sale.material_request_id.id})

        return super(StockPicking, self).create(vals)
    
    @api.onchange('analytic_accounts', 'analytic_tag_ids')
    def _onchange_analytic_accounts(self):
        for rec in self.move_ids_without_package:
            rec.update({'analytic_account_id': self.analytic_accounts.id,
                        'analytic_tag_ids': [(6, 0, self.analytic_tag_ids.ids)]})
