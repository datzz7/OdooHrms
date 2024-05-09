# -*- coding: utf-8 -*-

import datetime
from functools import reduce
from odoo import models
from odoo.exceptions import UserError


class SummaryListPurchase(models.AbstractModel):
    _name = 'report.briqx_vat_relief.summary_list_purchase'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, obj):
        sheet = workbook.add_worksheet('BIR SLP')
        bold = workbook.add_format({'bold': True, 'align': 'center', 'bg_color': '#fffbed', 'border': True})
        title = workbook.add_format({'bold': True, 'align': 'center', 'font_size': 20, 'bg_color': '#f2eee4', 'border': True})
        row = 0
        col = 0
        s_no = 1
        sheet.set_column(0, 0, 15)
        sheet.set_column(1, 1, 30)
        sheet.set_column(2, 2, 15)
        sheet.set_column(3, 3, 15)
        sheet.set_column(4, 4, 15)
        sheet.set_column(5, 5, 30)
        sheet.set_column(6, 6, 10)
        sheet.set_column(7, 7, 10)
        sheet.set_column(8, 8, 10)
        sheet.set_column(9, 9, 10)
        sheet.set_column(10, 10, 10)
        sheet.set_column(11, 11, 10)
        sheet.set_column(12, 12, 10)
        sheet.set_column(13, 13, 10)
        sheet.set_column(14, 14, 10)
        for rec in obj:
                tin = rec.vendor_tin if rec.vendor_tin else ''
                sheet.write(row, col, str(tin).replace('-','')),
                sheet.write(row, col+1, rec.company_name.name if rec.company_name.name else ''),
                sheet.write(row, col+2, rec.last_name if rec.last_name else ''),
                sheet.write(row, col+3, rec.first_name if rec.first_name  else ''),
                sheet.write(row, col+4, rec.middle_name if rec.middle_name  else ''),
                sheet.write(row, col+5, rec.address1 if rec.address1 else ''),
                sheet.write(row, col+6, rec.address2 if rec.address2 else ''),
                sheet.write(row, col+7, rec.exempt),
                sheet.write(row, col+8, rec.zero_rated),
                sheet.write(row, col+9, rec.services),
                sheet.write(row, col+10, rec.capital_goods),
                sheet.write(row, col+11, rec.other_capital_goods),
                sheet.write(row, col+12, rec.taxable_net_vat),
                sheet.write(row, col+13, rec.input_vat),
                sheet.write(row, col+14, rec.posting_date)

                s_no+=1
                row += 1

        