# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Custom Check Writer',
    'version': '1.0',
    'description': 'Custom placement of Check Writer',
    'author': 'DGPrime-James MICHAEL ORTIZ',
    'sequence': 1,
    'summary': '',
    'category':'Productivity',
    'websites': 'None',
    'description': "",
    'depends': ['account','stock','base','web'],
    'data': [
        'check_writer_custom.xml'
    ],
    'installable': True,
    'auto_install': False,
}
