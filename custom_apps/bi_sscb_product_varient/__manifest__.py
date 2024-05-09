# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    "name" : "Advance Product Attributes (Style, Size, Color, Brand)",
    "version": "13.0.0.0",
    'category': 'Sales',
    "summary": "This odoo app helps user to manage product attributed with advance options like, brand, style, size, and color. User can create and manage different brands styles, sizes, and colors for product, Add brand to main product and add style, size and color attributes, and variant will created with added attributes, User can see brand, style, size and color for particular product template and search for specific attribute value, User also can group by product variant by style, color, size and brand.",    
    "description": 
    """
         This odoo app helps user to manage product attributed with advance options like, brand, style, size, and color. User can create and manage different brands styles, sizes, and colors for product, Add brand to main product and add style, size and color attributes, and variant will created with added attributes, User can see brand, style, size and color for particular product template and search for specific attribute value, User also can group by product variant by style, color, size and brand.

User can select product and see brand, style and size and color on sale order line, User also can filter sales analysis report by brand, style, size and color option. 

    """,
    'author': 'BrowseInfo',
    'website': 'https://www.browseinfo.com',
    "price": 45,
    "currency": 'EUR',
    "depends": ["base", "sale_management","product_matrix","product"],
    "data": [
        "security/ir.model.access.csv",
        "data/sscb_data.xml",
        "views/custom_brand_views.xml",
        "views/custom_size_views.xml",
        "views/custom_color_views.xml",
        "views/custom_style_views.xml",
        "views/custom_brand_views.xml",
        "views/product_inherit_views.xml",
        "views/res_config_settings_inherit_views.xml",
        "views/sale_order_inherit_views.xml",
    ],
    "installable": True,
    "auto_install": False,
    "application": False,
    'live_test_url':'https://youtu.be/K02F_egehC4',
    "images":['static/description/Banner.png'],
}
