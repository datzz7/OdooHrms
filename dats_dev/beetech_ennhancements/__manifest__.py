# -*- coding: utf-8 -*-
{
    'name': "Beetech Enhancements",
    'summary': """
       """,
    'description': """
    """,
    'author': "Dats",
    'website': "http://www.digiprimeinc.com",
    'category': 'Enhancements',
    'version': '0.1',
    'depends': ['base', 'account', 'sale', 'bi_sscb_product_varient', 'purchase'],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'views/account_move.xml',
        'views/sale.xml',
        'views/shipping_status.xml',
        'views/purchase.xml',
        'views/stock_picking.xml',
        
    ],
}
