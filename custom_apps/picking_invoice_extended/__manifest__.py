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
    'name': 'Picking Invoice Extend',
    'version': '14.0.0.0',
    'category': 'Account',
    'summary': 'Using this module user can add Doc Type,Vehicale Plate,Driver and Helper into Invoice',
    'description': """Using this module user can add Doc Type,Vehicale Plate,Driver and Helper into Invoice.""",
    'author': 'Acespritech Solutions Pvt. Ltd.',
    'website': 'http://www.acespritech.com',
    'depends': ['base', 'account', 'picking_transmittal', 'bi_auto_invoice'],
    'data': [
        'views/account_move.xml',
    ],
    'demo': [],
    'images': [],
    'installable': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4
