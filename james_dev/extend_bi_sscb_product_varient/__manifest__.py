{
    'name': 'Extended - Advance Product Attributes (Style, Size, Color, Brand)',
    'version': '1.0',
    'description': '',
    'summary': '',
    'author': 'Briq - James',
    'category': '',
    'depends': [
        'bi_sscb_product_varient','stock','base',"sale"
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/product_department.xml',
        'views/product_division.xml',
        'views/product_template.xml',
        'views/menu_items.xml'
    ],

    'auto_install': False,
    'application': False,
}