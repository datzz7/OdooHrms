# -*- coding: utf-8 -*-
{
    'name': "Trading - Sales",
    'summary': """
        Sales enhancement for trading companies""",
    'description': """
    """,
    'author': "Dats",
    'website': "http://www.digiprimeinc.com",
    'category': 'Trading',
    'version': '0.1',
    'depends': ['base', 'sale', 'contacts'],
    'data': [
        'security/ir.model.access.csv',
        'views/sales_order_type.xml',
        'views/localize_address.xml',
        'views/sales_area.xml',
        'views/sales_order_line.xml',
        'views/sale_order.xml',
        'views/res_partner.xml',
        'views/res_users.xml',
        'views/account_move.xml'
    ],
}
