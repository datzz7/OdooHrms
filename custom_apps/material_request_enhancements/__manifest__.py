# -*- coding: utf-8 -*-
{
    'name': "material_request_enhancements",

    'summary': """
        Material request enhancements for tradingV14/BBQ Boss.
        """,

    'description': """
    """,
    'author': "Dats",
    'website': "http://www.DIGIPRIMEINC.com",
    'category': 'Enhancements',
    'version': '0.1',
    'depends': ['base','material_request','purchase','sale','account'],
    'data': [
        'security/ir.model.access.csv',
        'views/material_request.xml',
        'wizard/create_rfq.xml',
        'views/purchase_order.xml',
        'views/account_move.xml',
        'views/sale_order.xml',
        'views/stock_picking.xml'
    ],
}