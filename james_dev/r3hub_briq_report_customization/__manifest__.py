# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'R3Hub Custom REports',
    'version' : '1.1',
    'summary': 'Odoo Report Custom for R3Hub',
    'author':'Digiprime - James',
    'sequence': 10,
    'description': """
        This Module is for Customizing Odoo Desigin Existing Report Only.
    """,
    'category': '',
    'depends' : ['base','account','sale','purchase'],
    'data': [
        'report/delivery_slip.xml',
       'report/sale_order.xml',
       'report/header_footer.xml',
       'report/purchase_order.xml'
    ],
    'installable': True,
    'application': False,
    'auto_install': True,
    
}
