# -*- coding: utf-8 -*-
{
    'name': "wtax_payment_journal",
    'summary': """
        Dependencies:
        - pw_invoice_payment_reconcile
        """,
    'description': """
        Payment enhancements with witholding taxes
    """,
    'author': "Dats",
    'website': "http://www.digiprimeinc.com",
    'category': 'Payment',
    'version': '0.1',
    'depends': ['base', 'account', 'pw_invoice_payment_reconcile'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/account_tax.xml',
        'views/account_payment.xml',
        'views/account_move.xml',
    ],
}
