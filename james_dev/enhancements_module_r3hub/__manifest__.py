# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Enhancements Module for R3hub',
    'version': '1.0',
    'description': '''
        This module are the Enhancements and Customization for R3hub
    ''',
    'author': 'DGPrime-James MICHAEL ORTIZ',
    'sequence': 1,
    'summary': '',
    'category':'',
    'websites': 'None',
    'description': "",
    'depends': ['stock','base','account'],
    'data': [
        'views/stock_picking.xml',
        'views/sales_order.xml',
        'views/account_move.xml'
        # 'report/delivery_receipt.xml',  #exclude this
        # 'report/purchase_order.xml', #exclude this
        # 'report/delivery_slip.xml',
        # 'report/report.xml'
        ],
    'installable': True,
    'auto_install': False,
}
