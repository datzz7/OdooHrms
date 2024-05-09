# -*- coding: utf-8 -*-
#################################################################################
# Author      : Acespritech Solutions Pvt. Ltd. (<www.acespritech.com>)
# Copyright(c): 2012-Present Acespritech Solutions Pvt. Ltd.
# All Rights Reserved.
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#################################################################################

{
    'name': 'Sale Order Extend',
    'version': '14.0.0.0',
    'category': 'Sale',
    'summary': 'Using this module user can add country,vat and order type into Sale Order',
    'description': """Using this module user can add country,vat and order type into Sale Order. 
                        Also show Order Date,Quotation Date and Scheduled Delivery Date into Date format.""",
    'author': 'Acespritech Solutions Pvt. Ltd.',
    'website': 'http://www.acespritech.com',
    'depends': ['base', 'sale_management', 'sale', 'stock'],
    'data': [
        'views/sale.xml',
    ],
    'demo': [],
    'images': [],
    'installable': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4
