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
    'name': 'Invoice Dispatch Fleet',
    'version': '14.0.0.0',
    'category': 'Fleet',
    'summary': 'Using this module user can create Invoice Dispatch and also print a invoice dispatch report.',
    'description': """Using this module user can create Invoice Dispatch and also print a invoice dispatch report.""",
    'author': 'Acespritech Solutions Pvt. Ltd.',
    'website': 'http://www.acespritech.com',
    'depends': ['base', 'picking_invoice_extended'],
    'data': [
        'security/ir.model.access.csv',
        'data/dispatch.xml',
        'views/account_move.xml',
        'views/invoice_dispatch.xml',
        'report/custom_layout.xml',
        'report/report.xml',
        'report/invoice_dispatch_report.xml',
    ],
    'demo': [],
    'images': [],
    'installable': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4
