# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Inventory Report - Briq Module',
    'version': '1.0',
    'description': 'Generate Inventory Report Print OUT for Vans and Warehouse  ',
    'author': 'DGPrime-James MICHAEL ORTIZ',
    'sequence': 1,
    'summary': '',
    'category':'Productivity',
    'websites': 'None',
    'description': "",
    'depends': ['account','stock','base','web'],
    'data': [
        'security/ir.model.access.csv',    
        'report/report.xml',
        'report/inv_rep_wh.xml',
        'report/inv_rep_wh_blnk.xml',
        'report/inv_rep_van.xml',
        'report/inv_rep_van_2.xml',
        'wizard/wiz_invent_rep_wh.xml',
        'wizard/wiz_invent_rep_van.xml',
        'view/invent_rep.xml',
        'view/invent_rep_van.xml',
        'view/stock_quant.xml',
        'view/menu.xml',
        
        
       
    ],
    'installable': True,
    'auto_install': False,
}
