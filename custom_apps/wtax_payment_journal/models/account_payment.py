# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError


class AccountPayment(models.Model):
    _inherit = 'account.payment'
    
    tax_id = fields.Many2one('account.tax', string='Withholding Tax Rate')
    tax_amount = fields.Float('Withholding Tax Amount',compute="tax_calculate",digits=dp.get_precision('Product Price'))
    tax_type = fields.Char('Tax categ',compute="get_tax_type")
    
    
    @api.depends('journal_id')
    def get_tax_type(self):
        if self.partner_type =='customer':
            self.tax_type ='sale'
        if self.partner_type =='supplier':
            self.tax_type ='purchase'
        if self.partner_type ==False:
            self.tax_type ='none'
    
    
    @api.depends('tax_id','amount')
    def tax_calculate(self):
       for rec in self:
            tax_amount = 0
            if rec.tax_id:
                tax_amount = ((rec.amount*rec.tax_id.amount)/100)
            
            rec.tax_amount = tax_amount
            
    def _synchronize_to_moves(self, changed_fields):
        super(AccountPayment, self)._synchronize_to_moves(changed_fields)
        for pay in self.with_context(skip_account_move_synchronization=True):
            if not pay.tax_id:
                continue
            move = pay.move_id
            if move.state == 'posted':
                continue
            liquidity_lines, counterpart_lines, writeoff_lines = pay._seek_for_lines()
            if writeoff_lines:
                writeoff_amount = sum(writeoff_lines.mapped('amount_currency'))
                counterpart_amount = counterpart_lines['amount_currency']
                if writeoff_amount > 0.0 and counterpart_amount > 0.0:
                    sign = 1
                else:
                    sign = -1

                write_off_line_vals = {
                    'name': writeoff_lines[0].name,
                    'amount': writeoff_amount * sign,
                    'account_id': writeoff_lines[0].account_id.id,
                }
            else:
                write_off_line_vals = {}

            line_vals_list = pay._prepare_move_line_default_vals(
                write_off_line_vals=write_off_line_vals)

            wtax_val_list = []
            wtax_vals_list = pay._prepare_wtax_move_lines(wtax_val_list)

            if pay.payment_type == 'inbound':
                # Receive money.
                counterpart_amount = -pay.amount + pay.tax_amount
            elif pay.payment_type == 'outbound':
                # Send money.
                counterpart_amount = pay.amount - pay.tax_amount
            else:
                counterpart_amount = 0.0
            balance = pay.currency_id._convert(
                counterpart_amount, pay.company_id.currency_id, pay.company_id, pay.date)
            liquidity_lines.with_context(check_move_validity=False, skip_account_move_synchronization=True).write({
                'amount_currency': -counterpart_amount,
                'debit': balance < 0.0 and -balance or 0.0,
                'credit': balance > 0.0 and balance or 0.0
            })
            if writeoff_lines:
                for rec in wtax_vals_list:
                    print(rec["account_id"])
                    if writeoff_lines.account_id.id == rec["account_id"]:
                        writeoff_lines.with_context(check_move_validity=False, skip_account_move_synchronization=True).write({
                            'amount_currency': rec["amount_currency"],
                            'debit': rec["debit"],
                            'credit': rec["credit"]
                        })
                        print(writeoff_lines.account_id)
            else:

                for rec in wtax_vals_list:
                    rec.update({'move_id': pay.move_id.id})
                    self.env['account.move.line'].with_context(check_move_validity=False,
                                                               skip_account_move_synchronization=True).create(rec)


    def _synchronize_from_moves(self, changed_fields):
        ''' Update the account.payment regarding its related account.move.
        Also, check both models are still consistent.
        :param changed_fields: A set containing all modified fields on account.move.
        '''
        if self._context.get('skip_account_move_synchronization'):
            return

        for pay in self.with_context(skip_account_move_synchronization=True):
            move = pay.move_id
            move_vals_to_write = {}
            payment_vals_to_write = {}

            if 'journal_id' in changed_fields:
                if pay.journal_id.type not in ('bank', 'cash'):
                    raise UserError(
                        _("A payment must always belongs to a bank or cash journal."))

            if 'line_ids' in changed_fields:
                all_lines = move.line_ids
                liquidity_lines, counterpart_lines, writeoff_lines = pay._seek_for_lines()

                if len(liquidity_lines) != 1 or len(counterpart_lines) != 1:
                    raise UserError(_(
                        "The journal entry %s reached an invalid state relative to its payment.\n"
                        "To be consistent, the journal entry must always contains:\n"
                        "- one journal item involving the outstanding payment/receipts account.\n"
                        "- one journal item involving a receivable/payable account.\n"
                        "- optional journal items, all sharing the same account.\n\n"
                    ) % move.display_name)

                # if writeoff_lines and len(writeoff_lines.account_id) != 1:
                #     raise UserError(_(
                #         "The journal entry %s reached an invalid state relative to its payment.\n"
                #         "To be consistent, all the write-off journal items must share the same account."
                #     ) % move.display_name)

                if any(line.currency_id != all_lines[0].currency_id for line in all_lines):
                    raise UserError(_(
                        "The journal entry %s reached an invalid state relative to its payment.\n"
                        "To be consistent, the journal items must share the same currency."
                    ) % move.display_name)

                if any(line.partner_id != all_lines[0].partner_id for line in all_lines):
                    raise UserError(_(
                        "The journal entry %s reached an invalid state relative to its payment.\n"
                        "To be consistent, the journal items must share the same partner."
                    ) % move.display_name)

                if counterpart_lines.account_id.user_type_id.type == 'receivable':
                    partner_type = 'customer'
                else:
                    partner_type = 'supplier'

                liquidity_amount = liquidity_lines.amount_currency
                move_vals_to_write.update({
                    'currency_id': liquidity_lines.currency_id.id,
                    'partner_id': liquidity_lines.partner_id.id,
                })
                payment_vals_to_write.update({
                    # 'amount': abs(liquidity_amount),
                    'payment_type': 'inbound' if liquidity_amount > 0.0 else 'outbound',
                    'partner_type': partner_type,
                    'currency_id': liquidity_lines.currency_id.id,
                    'destination_account_id': counterpart_lines.account_id.id,
                    'partner_id': liquidity_lines.partner_id.id,
                })

            move.write(move._cleanup_write_orm_values(
                move, move_vals_to_write))
            pay.write(move._cleanup_write_orm_values(
                pay, payment_vals_to_write))

    def _prepare_wtax_move_lines(self, line_vals_list):
        wtax_id = self.tax_id
        wtax_inv_dist_ids = wtax_id.invoice_repartition_line_ids
        currency_id = self.currency_id.id
        if self.is_internal_transfer:
            if self.payment_type == 'inbound':
                liquidity_line_name = _('Transfer to %s', self.journal_id.name)
            else:  # payment.payment_type == 'outbound':
                liquidity_line_name = _(
                    'Transfer from %s', self.journal_id.name)
        else:
            liquidity_line_name = self.payment_reference
        payment_display_name = {
            'outbound-customer': _("Customer Reimbursement"),
            'inbound-customer': _("Customer Payment"),
            'outbound-supplier': _("Vendor Payment"),
            'inbound-supplier': _("Vendor Reimbursement"),
        }
        default_line_name = self.env['account.move.line']._get_default_line_name(
            payment_display_name['%s-%s' %
                                 (self.payment_type, self.partner_type)],
            self.amount,
            self.currency_id,
            self.date,
            partner=self.partner_id,
        )

        for inv_dist in wtax_inv_dist_ids:
            if inv_dist.repartition_type == 'tax':
                if self.payment_type == 'inbound':
                    w_taxAmt = -self.tax_amount * (inv_dist.factor_percent/100)
                elif self.payment_type == 'outbound':
                    w_taxAmt = self.tax_amount * (inv_dist.factor_percent/100)
                else:
                    w_taxAmt = 0.0
                w_tax_account_id = inv_dist.account_id
                balance = self.currency_id._convert(
                    w_taxAmt, self.company_id.currency_id, self.company_id, self.date)

                counterpart_amount_currency = w_taxAmt
                if balance != 0:
                    line_vals_list.append({
                        'name': liquidity_line_name or default_line_name,
                        'date_maturity': self.date,
                        'amount_currency': -counterpart_amount_currency,
                        'currency_id': currency_id,
                        'debit': balance < 0.0 and -balance or 0.0,
                        'credit': balance > 0.0 and balance or 0.0,
                        'partner_id': self.partner_id.id,
                        'account_id': w_tax_account_id.id,
                        'whtax': True

                    })
        return line_vals_list

    @api.onchange('partner_id', 'payment_type', 'partner_type')
    def _onchange_partner_id(self):
        res = super(AccountPayment, self)._onchange_partner_id()
        move_type = {'outbound': 'in_invoice', 'inbound': 'out_invoice'}
        AccountMoveLine = self.env['account.move.line']
        vals = []
        # Select feature start
        if move_type[self.payment_type] == 'out_invoice':
            AccountMoveLine = self.env['account.move.line'].search([('is_select', '=',True),
                                                                ('partner_id','=',self.partner_id.id),
                                                                ('account_id.internal_type','=','receivable'),
                                                                ('reconciled','=',False)])
        if move_type[self.payment_type] == 'in_invoice':
            AccountMoveLine = self.env['account.move.line'].search([('is_select', '=',True),
                                                            ('partner_id','=',self.partner_id.id),
                                                            ('account_id.internal_type','=','payable'),
                                                            ('reconciled','=',False)])
        # Select feature end 
        
        # append journal entries in payment
        for newline_id in AccountMoveLine:
            total_amt = abs(newline_id.debit - newline_id.credit)
            move_id = newline_id.move_id
            
            if newline_id.amount_residual:
                amount_residual = abs(newline_id.amount_residual)
                coeff_net = amount_residual / total_amt
            else:
                coeff_net = total_amt / total_amt
            if newline_id.move_id.state == 'posted' :
                vals.append((0,0, {
                    'payment_id': self.id,
                    'invoice_id': move_id.id,
                    'amount_total': total_amt,
                    'amount_residual': (total_amt * coeff_net) ,
                    'amount_untaxed': total_amt,
                }))
                
        self.write({'reconcile_invoice_ids': vals})
        
        return res
    
class AccountTax(models.Model):
    _inherit = 'account.tax'
    
    is_withholding_tax = fields.Boolean('Is withholding', default=False)