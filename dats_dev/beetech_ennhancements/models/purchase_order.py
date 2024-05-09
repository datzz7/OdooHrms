from odoo import api, models, fields, _


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    
    
    shipping_status = fields.Many2one(comodel_name='po.shipping.status', string="Shipping Status")
    tracking_number = fields.Char(string="Tracking Number")
    
    
class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'
    
    def _prepare_account_move_line(self, move=False):
        res = super(PurchaseOrderLine, self)._prepare_account_move_line(move)
        
        return res
    # def _prepare_account_move_line(self, move=False):
    #     self.ensure_one()
    #     aml_currency = move and move.currency_id or self.currency_id
    #     date = move and move.date or fields.Date.today()
    #     res = {
    #         'display_type': self.display_type,
    #         'sequence': self.sequence,
    #         'name': '%s: %s' % (self.order_id.name, self.name),
    #         'product_id': self.product_id.id,
    #         'product_uom_id': self.product_uom.id,
    #         'quantity': self.qty_to_invoice,
    #         'price_unit': self.currency_id._convert(self.price_unit, aml_currency, self.company_id, date, round=False),
    #         'tax_ids': [(6, 0, self.taxes_id.ids)],
    #         'analytic_account_id': self.account_analytic_id.id,
    #         'analytic_tag_ids': [(6, 0, self.analytic_tag_ids.ids)],
    #         'purchase_line_id': self.id,
    #     }
    #     if not move:
    #         return res

    #     if self.currency_id == move.company_id.currency_id:
    #         currency = False
    #     else:
    #         currency = move.currency_id

    #     res.update({
    #         'move_id': move.id,
    #         'currency_id': currency and currency.id or False,
    #         'date_maturity': move.invoice_date_due,
    #         'partner_id': move.partner_id.id,
    #     })
    #     raise UserWarning("TEST")
    #     return res