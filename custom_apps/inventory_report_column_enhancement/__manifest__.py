# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Inventory Report Column Enhancement',
    'version': '1.0',
    'description': 'New Column "Route Price per Unit", "Direct Price per Unit","Total Price Onhand Route Price","Total Price Onhand Direct Price"',
    'author': 'DGPrime-James MICHAEL ORTIZ',
    'sequence': 1,
    'summary': '',
    'category':'Productivity',
    'websites': 'None',
    'description': "",
    'depends': ['stock','base'],
    'data': ['views/stock_quant.xml'],
    'installable': True,
    'auto_install': False,
}
