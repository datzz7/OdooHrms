from odoo import models, fields, api, _
from odoo.exceptions import UserError

class AccountMoveInherit(models.Model):
    _inherit = 'account.move'

    analytic_account_id = fields.Many2one(
            "account.analytic.account",
            string="Analytic Account",
            store=True,
            # compute="_compute_analytic_account",
            # inverse="_inverse_analytic_account",
            help="This account will be propagated to all lines, if you need "
            "to use different accounts, define the account at line level.",
        )
    analytic_tag_ids = fields.Many2many(
        comodel_name='account.analytic.tag', string="Analytic Tags")
    sale_type = fields.Selection(selection=[('cash',"Cash"),('charge',"Charge")], string="Type")
    
    @api.model
    def create(self, vals):
        res = super(AccountMoveInherit, self).create(vals)
        if res.picking_id:
            res.update({'analytic_account_id': res.picking_id.analytic_accounts.id,
                'analytic_tag_ids': [(6, 0, res.picking_id.analytic_tag_ids.ids)]})
        return res
    
    @api.onchange('analytic_account_id', 'analytic_tag_ids')
    def _onchange_analytic_accounts(self):
        for rec in self.invoice_line_ids:
            rec.update({'analytic_account_id': self.analytic_account_id.id,
                        'analytic_tag_ids': [(6, 0, self.analytic_tag_ids.ids)]})


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'
    

    