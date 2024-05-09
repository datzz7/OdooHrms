# -*- coding: utf-8 -*-
{
    'name': "Invoice & Payment reports",
    'summary': """
        Reports:
        - Check writer
        - Check voucher
        - APV Voucher""",
    'description': """
    """,

    'author': "Dats",
    'website': "http://www.digiprimeinc.com",
    'category': 'Reports',
    'version': '0.1',
    'depends': ['base', 'account', 'wtax_payment_journal'],
    'data': [
        # 'security/ir.model.access.csv',
        'report/check_voucher_template.xml',
        'report/check_voucher_writer_report.xml',
        'report/check_writer_template.xml',
        'report/apv_report_template.xml'
    ],  
}
