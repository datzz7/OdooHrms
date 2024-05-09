# -*- coding: utf-8 -*-
{
    'name': "Generic Books of Accounts",
    'summary': """
        """,
    'description': """
    """,
    'author': "Dats",
    'website': "http://www.digiprimeinc.com",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base', 'account', 'sale', 'purchase', 'sh_pdc'],
    'data': [
        'security/ir.model.access.csv',
        'views/disbursements_book.xml',
        'views/sales_receipts.xml',
        'views/general_ledger.xml',
        'views/purchase_book.xml',
        'views/sales_book.xml',
        'views/menu.xml',
        'data/data.xml'
    ],
}
