{
    'name': 'Invoice Type',
    'version': '14.0',
    'description':'Add a field type for invoice if it is a Trust Recipt Aggreement & Customer invoice Form',
    'author': 'Digiprime - James',
    'website': '',
    'category': '',
    'depends': [
     'account','beetech_custom_reports'
    ],
    'data': [
        'views/account_move.xml',
        'report/account_report.xml'
    ],
    'auto_install': False,
    'application': False,
}