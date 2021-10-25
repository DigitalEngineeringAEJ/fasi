# -*- coding: utf-8 -*-

import base64
from odoo import api, fields, models, _
from dateutil.relativedelta import relativedelta
from datetime import date
from odoo.exceptions import ValidationError
from collections import defaultdict
import calendar

class GefahrstoffVerzeichnis(models.Model):
    _name = 'gefahrstoff.verzeichnis'
    _description = 'Gefahrstoff Verzeichnis'

    name = fields.Char(string='Arbeitsbereich')
    
    id = fields.Char(string='Identifikation')
    
    sequence = fields.Integer(string='Sequenz')
    
    prod_bez = fields.Char(string='Stoff-/Produkt-bezeichnung(Handelsname,Produkt-Nr.)')
    
    partner_id = fields.Many2one('res.partner', string='Hersteller/Lieferant')
    
    kategorie = fields.Selection([('Flamme (GHS02)', 'Flamme (GHS02)'),
                                ('Gesund-heitsgefahr (GHS08)', 'Gesund-heitsgefahr (GHS08)'),
                                ('Umwelt (GHS09)', 'Umwelt (GHS09)'),
                                ('Ausrufezeichen (GHS07)', 'Ausrufezeichen (GHS07)'),
                                ('H226', 'H226'),
                                ('H304', 'H304'),
                                ('H335', 'H335'),
                                ('H336', 'H336'),
                                ('H411', 'H411'),
                                ],
                                string='Einstufung, gefährliche Eigenschaften',)
    kategorie_ids = fields.One2many('gefahrstoff.kategorie','name' ,string="kategorie")
        
    zweck = fields.Char(string='Verwendungszweck/Arbeitsverfahren')
    
    menge = fields.Char(string='Im Betrieb verwendete Mengenbereiche pro Jahr(l, kg, t)')
    
    zeitraum = fields.Date(string='Verwendungszeitraum')
    
    daten_blatt = fields.Date(string='Sicherheitsdatenblatt vom')
    
class GefahrstoffVerzeichnisKategorie(models.Model):
    _name = 'gefahrstoff.kategorie'
    _description = 'Gefahrstoff Verzeichnis Kategorie'
    
    name = fields.Char(string='Gefahrstoff Verzeichnis Kategorie')
    
    flamme = fields.Boolean(string='Flamme (GHS02)')
    
    gesundheitsgefahr = fields.Boolean(string='Gesund-heitsgefahr (GHS08)')
    
    umwelt = fields.Boolean(string='Umwelt (GHS09)')
    
    ausrufezeichen = fields.Boolean(string='Ausrufezeichen (GHS07)')
    
    h_zwei_zwei_sechs = fields.Boolean(string='H226')
    
    h_drei_null_vier = fields.Boolean(string='H304')
    
    h_drei_drei_fünf = fields.Boolean(string='H335')
    
    h_drei_drei_sechs = fields.Boolean(string='H336')
    
    h_vier_eins_eins = fields.Boolean(string='H411')
    
    
    