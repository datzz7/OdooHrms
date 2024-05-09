# -*- coding: utf-8 -*-

{
    "name": " Briqx Debranding",
    'version': '14.1.0.0',
    "description": """This module can be used for Debranding Odoo for front-end and back-end """,
    'summary': """To Configure go to System paramaters and choose your brand name""",
    'author': 'Digiprime Incorporated',
    'company': "www.digiprimeinc.com",
    'category': "Extra Tools",
    "license": "AGPL-3",
    'depends': [
        'web',
        'mail',
        'base_setup',
        'mail_bot',
        'portal',

    ],
    'data': [
        # 'views/data.xml',
        'views/views.xml',
        'views/js.xml',
        'views/res_config_settings_view.xml',
        'security/ir.model.access.csv',
        'views/title.xml',
        'views/portal_templates.xml',
        'views/brand_promotion.xml',
        'views/login_layout.xml',
        ],
    'qweb': [
        'static/src/xml/web.xml',
        'static/src/xml/dashbord.xml',
        'static/src/xml/res_config_edition.xml',

    ],
    'images': ['static/description/main.png'],
    'auto_install': False,
    'installable': True,
    'application': True,

}
