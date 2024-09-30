# -*- coding: utf-8 -*-
{
    'name': "Real Estate Ads",

    'summary': """
        Module to manage for sale properties """,

    'description': """
        Module to manage properties ads
    """,

    'author': "PT Ikki",
    'website': "https://www.mycompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/res_groups.xml',
        
        'views/property_view.xml',
        'views/property_type_view.xml',
        'views/property_tag_view.xml',
        'views/property_offer_view.xml',
        'views/menu_items.xml',
        'views/templates.xml',

        # Data Files
        # 'data/property_type.xml',
        'data/estate.property.type.csv'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/property_tag.xml',
    ],

    'application': True,
}
