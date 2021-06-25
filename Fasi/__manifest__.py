# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Fasi',
    'version' : '0.1',
    'summary': 'Invoices & Payments',
    'author': "Digital Engineering AEJ",
    'sequence': 10,
    'description': """""",
    'category': 'Accounting/Accounting',
    'images': [],
    'depends': ['base_setup'],
    'data': [],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'post_init_hook': '_account_post_init',
}
