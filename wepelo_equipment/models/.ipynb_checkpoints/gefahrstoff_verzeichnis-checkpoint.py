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
    
    zweck = fields.Char(string='Verwendungszweck/Arbeitsverfahren')
    
    menge = fields.Char(string='Im Betrieb verwendete Mengenbereiche pro Jahr(l, kg, t)')
    
    zeitraum = fields.Date(string='Verwendungszeitraum')
    
    daten_blatt = fields.Date(string='Sicherheitsdatenblatt vom')
    
    
    