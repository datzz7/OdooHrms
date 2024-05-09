# -*- coding: utf-8 -*-
{
    'name': 'Create Purchase Order from Sale Order',
    'category': 'Purchase',
    'summary': 'Create Purchase Order from Sale Order | Purchase order from Sale Order | Create PO from SO | Create Sale Order to Purchase Order | easy to Create Sale Orders to Purchase Order',
    'description': """
This module help you create purchase order from sale order""",
    'author': 'Preway IT Solutions',
    'version': '1.0',
    'depends': ['purchase','sale_management'],
    "data": [
        'security/ir.model.access.csv',
        'security/purchase_security.xml',
        'wizard/purchase_order_wizard_view.xml',
        'views/sale_order_view.xml',
        'views/purchase_order_view.xml',
    ],
    'price': 10.0,
    'currency': 'EUR',
    'installable': True,
    'auto_install': False,
    'application': True,
    "license": "LGPL-3",
    "images":["static/description/Banner.png"],
}
