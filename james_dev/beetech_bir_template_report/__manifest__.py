# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'BIR Template Reports - Briq Module',
    'version': '1.0',
    'description': 'Default Report Template BIR',
    'author': 'DGPrime-James MICHAEL ORTIZ',
    'sequence': 1,
    'summary': '',
    'category':'Productivity',
    'websites': 'None',
    'description': "",
    'depends': ['base','account','web','pw_invoice_payment_reconcile'],
    'data': [
        'view/vendor_bill.xml',
        'report/report.xml',
        'report/bir_sales_invoice.xml',
        'report/bir_composition_cas_apv.xml',
        'report/bir_collection_receipt.xml',
        'report/bir_official_receipt.xml',
        'report/bir_withholding_2307.xml',
        'report/bir_check_voucher.xml',
        'report/bir_invoice_w_payments.xml'
    ],
    'installable': True,
    'auto_install': False,
}
