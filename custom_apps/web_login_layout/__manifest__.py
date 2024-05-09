{
    'name': 'Background Web Login',
    'category': 'Web',
    'summary': 'Background Image with Multi layout',
    'version': '14.0.0.1',
    'license': 'OPL-1',    
    
    'author': 'Lumynos Technologies',
    'website': 'https://www.lumynostechnologies.com',

    'depends': [
        'base_setup', 'briqx_debranding',      
    ],

    'data': [
        'view/res_config_settings_view.xml',
        'templates/inherited_login_layout.xml',
    ],

    'images': [
        'static/description/Banner.jpg',
    ],
    
    'installable': True,
    'auto_install': False,
    'price': 25.00,
    'currency': 'USD',  
}
