# -*- coding: utf-8 -*-

{
    'name': 'Safety Master',
    'version': '0.12',
    'category': 'Services',
    'author': "JADESi",
    'description': """Anwendung zu Organisation von Tätigkeiten für den Arbeitsschutz""",
    'depends': ['maintenance', 'portal'],
    'summary': 'Application for organizing activities for occupational safety',
    'website': 'JADESi',
    'data': [
        'security/ir.model.access.csv',
        'data/wepelo_mail_data.xml',
        'views/assets.xml',
        'views/maintenance_equipment_category_views.xml',
        'views/wepelo_maintenance_views.xml',
        'wizard/mail_activity_edit_wizard_views.xml',
        'views/mail_activity_views.xml',
        'report/wepelo_equipment_protocol_report.xml',
        'report/wepelo_equipment_protocol_bremsprufstand_report.xml',
        'report/wepelo_equipment_eichnachweis_protocol_report.xml',
        'report/wepelo_equipment_protocol_maintenance_report.xml',
        'report/wepelo_equipment_protocol_hebebuhne_report.xml',
        'report/wepelo_equipment_protocol_tore_report.xml',
        'report/wepelo_equipment_protocol_rep_report.xml',
        'report/wepelo_equipment_protocol_rep_prot_report.xml',
        'report/wepelo_maintenance_equipment_strichcode.xml',
        'views/menu.xml',
        'views/wepelo_equipment_protocol_views.xml',
        'views/wepelo_repair_view.xml',
        'views/wepelo_customer_view.xml',
        'views/equipment_portal_templates.xml',
        'views/res_users_views.xml',
        'views/maintenance_equipment_category_views.xml'
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False
}