# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, models


class report_check_writer(models.AbstractModel):
    _name = 'report.invoice_payment_reports.report_check_writer'

    def _get_report_values(self, docids, data=None):
        model = self.env['account.payment']
        payment= []
        for payment_id in docids:
            account_payment = model.search([('id', '=', payment_id)])
            payment.append(account_payment)
        return {
               'doc_ids': docids,
               'doc_model': model,
               'docs': payment,
               }
