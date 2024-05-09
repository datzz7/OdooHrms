{
    'name': 'Project Qoutation',
    'version': '14.0',
    'description': '''
        Project Qoutation is a sales and purchase module but with different type it will include services and it will group the itemize 
    ''',
    'summary': 'Project Qoutation it is a type of sales qoutation and purchase qoutation',
    'author': 'Digiprime - James Michael Ortiz',
    'category': '',
    'depends': [
        'sale','purchase','base'
    ],'data':[
        'data/ir_sequence_data.xml',
        'views/sale.xml',
        # 'views/purchase.xml',
        'views/menu_item.xml',
        'report/report_sale.xml'
    ],
    'auto_install': False,
    'application': False,
    
}