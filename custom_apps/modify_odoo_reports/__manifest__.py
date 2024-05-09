# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Modify Existing Odoo Reports for BBQ BOSS',
    'version': '1.0',
    'summary': '',
    'author': 'DIGIPRIME - JAMES MICHAEL ORTIZ',
    'depends': [
        'account','base','stock','stock_account','pw_invoice_payment_reconcile'
    ],
    'data': [
        'views/product_template.xml',
        'views/stock_valuation_layer.xml',
        'reports/check_voucher.xml',
        'reports/product_countsheet.xml',
        'reports/report.xml'
        
        
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
