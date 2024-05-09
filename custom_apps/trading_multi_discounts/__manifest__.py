# -*- coding: utf-8 -*-
{
    'name': "Trading - Multi Discounts",
    'summary': """
        Multi discounts module for trading Companies.""",
    'description': """
    """,
    'author': "Dats",
    'website': "http://www.digiprimeinc.com",
    'category': 'Trading',
    'version': '0.1',
    'depends': ['base', 'sale', 'account', 'trading_sales'],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order.xml',
        'views/account_move.xml'
    ],
}
