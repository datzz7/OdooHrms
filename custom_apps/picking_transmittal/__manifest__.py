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
    'name': 'Picking Transmittal',
    'version': '14.0.0.0',
    'category': 'Inventory',
    'summary': 'Using this module user can create Picking Transmittals.',
    'description': """Using this module user can create Picking Transmittals. 
                        Also show Received Picking List and Unserved Stock List.""",
    'author': 'Acespritech Solutions Pvt. Ltd.',
    'website': 'http://www.acespritech.com',
    'depends': ['base', 'sale', 'stock', 'fleet', 'so_extended', 'localize_address'],
    'data': [
        'security/transmittal_security.xml',
        'security/ir.model.access.csv',
        'data/transmittal.xml',
        'views/area_country.xml',
        'views/picking_transmittal.xml',
        'views/fleet_vehicle.xml',
        'views/stock_picking.xml',
        'wizard/stock_backorder_confirmation.xml',
        'views/unserved_stock_list.xml',
        'report/custom_layout.xml', 
        'report/picking_transmittal_report.xml',
        'report/report.xml',
        
    ],
    'demo': [],
    'images': [],
    'installable': True,
    'auto_install': False,
}
