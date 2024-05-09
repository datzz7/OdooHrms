# -*- coding: utf-8 -*-
{
    'name': "Trading - Free Goods",
    'summary': """
        Free goods for trading companies""",
    'description': """
    """,
    'author': "Dats",
    'website': "http://www.digiprimeinc.com",
    'category': 'Trading',
    'version': '0.1',
    'depends': ['base', 'sale', 'stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order.xml',
        'views/stock_picking.xml'
    ],
}
