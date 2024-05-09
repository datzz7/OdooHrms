# -*- coding: utf-8 -*-
{
    'name': "BIR SLS/SLP",
    'summary': """
        Module References:
        - briqx_vat_relief
        """,
    'description': """
    """,
    'author': "Dats",
    'website': "http://www.digiprimeinc.com",
    'category': 'Enhancements',
    'version': '0.1',
    'depends': ['base', 'account', 'purchase', 'sale', 'l10n_ph'],
    'data': [
        'security/ir.model.access.csv',
        'views/account_move.xml',
        'views/bir_summary_list_sales.xml',
        'views/bir_summary_list_purchase.xml',
        'views/menu.xml',
    ],
}
