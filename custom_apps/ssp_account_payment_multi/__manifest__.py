# -*- coding: utf-8 -*-
# Copyright 2021 SystemSolutions.pro. - Ing Henry Vivas
{
    "name": "Multiple and Partial Invoice Payment",
    "version": "14.2.2.3",
    "description": """
        Multiple Pay or Pay Partial for Invoice Document Customer and Vendor.
    """,
    'price': 35,
    'currency': 'EUR',
    'license': 'OPL-1',
    "author" : "SystemSolutions PRO",
    'sequence': 30,
    "email": 'controlwebmanger@gmail.com',
    "website":'http://SystemSolutions.pro/',
    'live_test_url': 'https://demo.systemsolutions.pro/',
    'category':"Accounting",
    'summary':"Using this module you can pay complete or partial pay multiple invoice payment in one click.",
    "depends": [
        "account",
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/account_assets.xml',
        'views/account_payment_view.xml',
        'wizard/account_payment_register_view.xml'
    ],
    'qweb': [
        "static/src/xml/account_payment.xml",
    ],
    "images": ['static/description/main_screenshot.png'],
    'installable': True,
    'auto_install': False,
}

