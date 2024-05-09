{
    'name': 'Reports and Modified Reports for Beetech',
    'version': '14.0',
    'description': 'This Module is for Beetech Reports',
    'summary': '',
    'author': 'Digiprime James',
    'category': '',
    'depends': [
        'stock','base','account','beetech_ennhancements','purchase'
    ],
    'data': [
       'reports/report.xml',
        'reports/header_footer.xml',
        'reports/beetach_sales_report.xml',
        'reports/beetech_purchase_report.xml',
        'reports/beetech_account_move.xml', #for T2403-001231
        'reports/beetech_delivery_orders.xml',
        'reports/beetech_delivery_reciept.xml',
         


    ],
    'auto_install': True,
    'application': False,
   
}