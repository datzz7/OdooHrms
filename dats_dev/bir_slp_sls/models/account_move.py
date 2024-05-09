# -*- coding: utf-8 -*-

from odoo import models, api, fields, _
from odoo.exceptions import UserError
from collections import defaultdict

class AccountMove(models.Model):
    _inherit = 'account.move'
    
    exempt = fields.Float(compute='_compute_bir_tax_amounts')
    zero_rated = fields.Float(compute='_compute_bir_tax_amounts')
    vatable_amount = fields.Float(compute='_compute_bir_tax_amounts')
    wtax_amount_total = fields.Float(compute='_compute_wtax_amount_total')
    
    @api.onchange('invoice_line_ids')
    def _onchange_invoice_line_ids(self):
        current_invoice_lines = self.line_ids.filtered(lambda line: not line.exclude_from_invoice_tab or 'WTAX' in line.name if line.name else '')
        others_lines = self.line_ids - current_invoice_lines
        if others_lines and current_invoice_lines - self.invoice_line_ids:
            others_lines[0].recompute_tax_line = True
        
        self.line_ids = others_lines + self.invoice_line_ids
        # Dats custom for wtax start
        tax_account = {}
        wtax_data = []
        if self.wtax_amount_total:
            for lines in self.invoice_line_ids:
                for tax in lines.wtax_id.invoice_repartition_line_ids:
                    tax_account['id'] = tax.account_id.id
                    tax_account['amount'] = lines.wtax_id.amount
                    # tax_account.append({'id': tax.account_id.id,
                    #                     'amount': lines.wtax_id.amount})
                    
                if lines.wtax_id:
                    wtax_data.append((0, 0, {
                                    'name': "{}% WTAX".format(tax_account['amount']),
                                    'account_id':  tax_account['id'],
                                    'exclude_from_invoice_tab': True,
                                    'price_unit': -abs(lines.wtax_amount),
                                    'credit': abs(lines.wtax_amount),
                                    'currency_id': self.currency_id.id,
                                    }))
                
            self.update({'line_ids': wtax_data,})
        # Dats custom for wtax end
                
        self._onchange_recompute_dynamic_lines()
        
    
    @api.depends('amount_total', 'invoice_line_ids', 'invoice_line_ids.wtax_id')
    def _compute_wtax_amount_total(self):
        for rec in self:
            wtax_amount = 0
            
            for lines in rec.invoice_line_ids:
                if lines.wtax_id:
                    wtax_amount += lines.wtax_amount
                    
            rec.wtax_amount_total = wtax_amount
            
    
    def action_post(self):
        res = super(AccountMove, self).action_post()
        
        for rec in self:
            services = 0.00
            capital = 0.00
            otcapital = 0.00
            taxable_net_vat = 0.00
            slp = rec._prepare_bir_summary_data()
            for lines in rec.invoice_line_ids:
                taxable_net_vat += lines.price_subtotal if lines.tax_ids else 0
                
                if lines.product_id.type in ['consu', 'product'] :
                    otcapital += lines.price_subtotal
                if lines.product_id.type == 'capital':
                    capital += lines.price_subtotal
                if lines.product_id.type == 'service':
                    services += lines.price_subtotal
                
            if rec.move_type == 'in_invoice':
                slp['capital_goods'] = capital if rec.partner_id.company_type == 'company' else 0.00
                slp['services'] = services
                slp['vendor_tin'] = self.partner_id.vat
                slp['other_capital_goods'] = otcapital if rec.partner_id.company_type == 'company' else 0.00
                slp['vat_rate'] = 0.00
                slp['input_vat'] = self.amount_tax
                slp['taxable_net_vat'] = taxable_net_vat
                slp['total_purchases'] = rec.exempt + rec.zero_rated + services + capital + otcapital
                self.env['bir.slp'].create(slp)
                
            if rec.move_type == 'out_invoice':
                slp['client_tin'] = self.partner_id.vat
                slp['output_vat'] = rec.amount_tax
                slp['total_sales'] = rec.amount_untaxed
                slp['gross_taxable'] = rec.amount_untaxed + rec.amount_tax
                slp['taxable_net_vat'] = taxable_net_vat
                self.env['bir.sls'].create(slp)
        
        return res
    
    def _prepare_bir_summary_data(self):
        partner = self.partner_id
        return {
            'account_invoice_id': self.id,
            'posting_date': fields.date.today(),
            'company_name': partner.id,
            'last_name': partner.last_name if self.partner_id.company_type != 'company' else '',
            'first_name': partner.first_name if self.partner_id.company_type != 'company' else '',
            'middle_name': partner.middle_name if self.partner_id.company_type != 'company' else '',
            'address1': partner.street,
            'address2': partner.street2,
            'exempt': self.exempt,
            'zero_rated': self.zero_rated,
        }
    
    @api.depends('invoice_line_ids', 'amount_untaxed')
    def _compute_bir_tax_amounts(self):
        for rec in self:
            zero_rated = 0.00
            exempt = 0.00
            vatable = 0.00
                    
            for lines in rec.invoice_line_ids:
                if 'Vat Exempt' in lines.account_id.name:
                    exempt += lines.price_subtotal
                
                if 'Zero Rated' in lines.account_id.name:
                    zero_rated += lines.price_subtotal
                            
                if lines.tax_ids:
                    vatable += lines.price_subtotal
                    
            rec.exempt = exempt
            rec.vatable_amount = vatable
            rec.zero_rated = zero_rated
    
    def button_draft(self):
        res = super(AccountMove, self).button_draft()
        slp_rec = self.env['bir.slp'].search([('account_invoice_id', '=', self.id)])
        sls_rec = self.env['bir.sls'].search([('account_invoice_id', '=', self.id)])
        
        if slp_rec:
            for lines in slp_rec:
                lines.unlink()
                
        if sls_rec:
            for lines in sls_rec:
                lines.unlink()
                
        return res
    
    
    @api.depends(
        'line_ids.matched_debit_ids.debit_move_id.move_id.payment_id.is_matched',
        'line_ids.matched_debit_ids.debit_move_id.move_id.line_ids.amount_residual',
        'line_ids.matched_debit_ids.debit_move_id.move_id.line_ids.amount_residual_currency',
        'line_ids.matched_credit_ids.credit_move_id.move_id.payment_id.is_matched',
        'line_ids.matched_credit_ids.credit_move_id.move_id.line_ids.amount_residual',
        'line_ids.matched_credit_ids.credit_move_id.move_id.line_ids.amount_residual_currency',
        'line_ids.debit',
        'line_ids.credit',
        'line_ids.currency_id',
        'line_ids.amount_currency',
        'line_ids.amount_residual',
        'line_ids.amount_residual_currency',
        'line_ids.payment_id.state',
        'line_ids.full_reconcile_id',
        'line_ids.wtax_id')
    def _compute_amount(self):
        in_invoices = self.filtered(lambda m: m.move_type == 'in_invoice')
        out_invoices = self.filtered(lambda m: m.move_type == 'out_invoice')
        others = self.filtered(lambda m: m.move_type not in ('in_invoice', 'out_invoice'))
        reversed_mapping = defaultdict(lambda: self.env['account.move'])
        for reverse_move in self.env['account.move'].search([
            ('state', '=', 'posted'),
            '|', '|',
            '&', ('reversed_entry_id', 'in', in_invoices.ids), ('move_type', '=', 'in_refund'),
            '&', ('reversed_entry_id', 'in', out_invoices.ids), ('move_type', '=', 'out_refund'),
            '&', ('reversed_entry_id', 'in', others.ids), ('move_type', '=', 'entry'),
        ]):
            reversed_mapping[reverse_move.reversed_entry_id] += reverse_move

        caba_mapping = defaultdict(lambda: self.env['account.move'])
        caba_company_ids = self.company_id.filtered(lambda c: c.tax_exigibility)
        reverse_moves_ids = [move.id for moves in reversed_mapping.values() for move in moves]
        for caba_move in self.env['account.move'].search([
            ('tax_cash_basis_move_id', 'in', self.ids + reverse_moves_ids),
            ('state', '=', 'posted'),
            ('move_type', '=', 'entry'),
            ('company_id', 'in', caba_company_ids.ids)
        ]):
            caba_mapping[caba_move.tax_cash_basis_move_id] += caba_move

        for move in self:

            if move.payment_state == 'invoicing_legacy':
                # invoicing_legacy state is set via SQL when setting setting field
                # invoicing_switch_threshold (defined in account_accountant).
                # The only way of going out of this state is through this setting,
                # so we don't recompute it here.
                move.payment_state = move.payment_state
                continue

            total_untaxed = 0.0
            total_untaxed_currency = 0.0
            total_tax = 0.0
            total_tax_currency = 0.0
            total_to_pay = 0.0
            total_residual = 0.0
            total_residual_currency = 0.0
            total = 0.0
            total_currency = 0.0
            currencies = move._get_lines_onchange_currency().currency_id

            for line in move.line_ids:
                if move.is_invoice(include_receipts=True):
                    # === Invoices ===

                    if not line.exclude_from_invoice_tab:
                        # Untaxed amount.
                        total_untaxed += line.balance
                        total_untaxed_currency += line.amount_currency
                        total += line.balance
                        total_currency += line.amount_currency
                    elif line.tax_line_id:
                        # Tax amount.
                        total_tax += line.balance
                        total_tax_currency += line.amount_currency
                        total += line.balance
                        total_currency += line.amount_currency
                    elif line.account_id.user_type_id.type in ('receivable', 'payable'):
                        # Residual amount.
                        total_to_pay += line.balance
                        total_residual += line.amount_residual
                        total_residual_currency += line.amount_residual_currency
                else:
                    # === Miscellaneous journal entry ===
                    if line.debit:
                        total += line.balance
                        total_currency += line.amount_currency

            if move.move_type == 'entry' or move.is_outbound():
                sign = 1
            else:
                sign = -1
            move.amount_untaxed = sign * (total_untaxed_currency if len(currencies) == 1 else total_untaxed)
            move.amount_tax = sign * (total_tax_currency if len(currencies) == 1 else total_tax)
            move.amount_total = sign * (total_currency if len(currencies) == 1 else total) 
            move.amount_residual = -sign * (total_residual_currency if len(currencies) == 1 else total_residual)
            move.amount_untaxed_signed = -total_untaxed
            move.amount_tax_signed = -total_tax
            move.amount_total_signed = abs(total) if move.move_type == 'entry' else -total
            move.amount_residual_signed = total_residual

            currency = len(currencies) == 1 and currencies or move.company_id.currency_id

            # Compute 'payment_state'.
            new_pmt_state = 'not_paid' if move.move_type != 'entry' else False

            if move.is_invoice(include_receipts=True) and move.state == 'posted':

                if currency.is_zero(move.amount_residual):
                    reconciled_payments = move._get_reconciled_payments()
                    if not reconciled_payments or all(payment.is_matched for payment in reconciled_payments):
                        new_pmt_state = 'paid'
                    else:
                        new_pmt_state = move._get_invoice_in_payment_state()
                elif currency.compare_amounts(total_to_pay, total_residual) != 0:
                    new_pmt_state = 'partial'

            if new_pmt_state == 'paid' and move.move_type in ('in_invoice', 'out_invoice', 'entry'):
                reverse_moves = reversed_mapping[move]
                caba_moves = caba_mapping[move]
                for reverse_move in reverse_moves:
                    caba_moves |= caba_mapping[reverse_move]

                # We only set 'reversed' state in cas of 1 to 1 full reconciliation with a reverse entry; otherwise, we use the regular 'paid' state
                # We ignore potentials cash basis moves reconciled because the transition account of the tax is reconcilable
                reverse_moves_full_recs = reverse_moves.mapped('line_ids.full_reconcile_id')
                if reverse_moves_full_recs.mapped('reconciled_line_ids.move_id').filtered(lambda x: x not in (caba_moves + reverse_moves + reverse_moves_full_recs.mapped('exchange_move_id'))) == move:
                    new_pmt_state = 'reversed'

            move.payment_state = new_pmt_state
            
    
    