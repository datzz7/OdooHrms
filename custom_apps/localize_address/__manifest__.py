# -*- coding: utf-8 -*-
{
    'name': "PH Localized Address",

    'summary': """
        PH Standard Localized Address""",
    'website': "digiprimeinc.com",
    'description': """
        The following are added:
            * Continents
            * Continent Regions
            * Countries
            * Island Groups
            * Regional Clusters
            * States/Regions
            * Provinces
            * Cities
            * Barangay
    """,

    'author': "Elms",
    'category': 'Accounting',
    'version': '0.1',
    'depends': [
        'base',
        'contacts',
        ],
    'data': [
        'security/ir.model.access.csv',
        'views/localize_address.xml',

    ],
    'installable': True,
    'auto_install': False,
}
