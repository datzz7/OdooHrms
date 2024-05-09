# -*- coding: utf-8 -*-
{
    'name': "Product Varient module extend (Dats)",

    'summary': """ """,
    'description': """
    """,
    'author': "Dats",
    'website': "http://www.digiprimeinc.com",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base', 'account', 'bi_sscb_product_varient', 'extend_bi_sscb_product_varient', 'sale'],
    'data': [
        'security/ir.model.access.csv',
        'report/sale.xml',
        'views/product_product.xml',
        'views/variant_model.xml',
        'views/variant_warranty.xml',
        'views/menu.xml',
        'views/sale_order.xml',
        'views/account_move.xml'
    ],
}
