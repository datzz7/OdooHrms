# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, models,_
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)

class report_check_voucher_bbqboss(models.AbstractModel):
    _name = 'report.modify_odoo_reports.report_check_voucher_bbqboss'

    def _get_report_values(self, docids, context=None,data=None):
        models = self.env['account.payment']
        payment_dict = {}
        account_payment = []
        invoice_move_line = {}
        for payment_id in docids:
            # debit = 0
            # credit = 0
            # account_payment_line = []
            account_payment_id = models.search([('id', '=', payment_id)])
            account_payment.append(account_payment_id)
            # account_move = self.env['account.move'].search([('name','=',account_payment_id.name)])
            # account_move_line = self.env['account.move.line'].search([('move_id','=',account_move.id)])
            # account_payment_line.append(account_move_line)


            invoice_move = self.env['account.move'].search([('name','=',account_payment_id.move_id.ref)])
            invoice_move_line = self.env['account.move.line'].search([('move_id','=',invoice_move.id),('exclude_from_invoice_tab','=',False)])
            # _logger.info('logs invoice_move: %s'%(invoice_move))
            # for line in account_move_line:
            #     debit = debit + line.debit
            #     credit = credit + line.credit
            # payment_dict[account_payment_id.id] = account_payment_line
            # payment_dict['credit'+str(account_payment_id.id)] = credit
            # payment_dict['debit'+str(account_payment_id.id)] = debit
        data = {
                   'doc_ids': docids,
                   'doc_model': models,
                   'docs': account_payment,
                #    'payment_dict': payment_dict,
                   'account_move_line': invoice_move_line,
                   'account_move':invoice_move
            }
        return data
