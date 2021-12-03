# -*- coding: utf-8 -*-

{
    'name': 'Safety Master',
    'version': '0.12',
    'category': 'Services',
    'author': "JADESi",
    'description': """Anwendung für die Arbeitsabläufe in der Arbeitssicherheit""",
    'depends': ['maintenance', 'portal'],
    'summary': 'Anwendung für die Arbeitsabläufe in der Arbeitssicherheit',
    'website': 'https://www.jadesi.de',
    'data': [
        'security/ir.model.access.csv',
        'data/wepelo_mail_data.xml',
        'views/assets.xml',
        'views/maintenance_equipment_category_views.xml',
        'views/wepelo_maintenance_views.xml',
        'wizard/mail_activity_edit_wizard_views.xml',
        'views/mail_activity_views.xml',
        'report/begehung_safety_master.xml',
        'report/wepelo_maintenance_equipment_strichcode.xml',
        'report/folgebegehung_safety_master.xml',
        'report/gefaerdungsbeurteilung_safety_master.xml',
        'report/protocol_betriebsanweisung_template.xml',
        'report/gefahrstoff_verzeichnis.xml',
        'report/unterweisung.xml',
        'report/safety_master_betriebsanweisung_gefahrstoffe.xml',
        'report/safety_master_betriebsanweisung_psa.xml',
        'views/menu.xml',
        'views/wepelo_equipment_protocol_views.xml',
        'views/wepelo_repair_view.xml',
        'views/wepelo_customer_view.xml',
        'views/equipment_portal_templates.xml',
        'views/res_users_views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False
}