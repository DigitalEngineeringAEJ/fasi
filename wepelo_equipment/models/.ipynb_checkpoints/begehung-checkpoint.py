# -*- coding: utf-8 -*-

import base64
from odoo import api, fields, models, _
from dateutil.relativedelta import relativedelta
from datetime import date
from odoo.exceptions import ValidationError
from collections import defaultdict
import calendar

class Begehung(models.Model):
    _name = 'begehung'
    _description = 'Aktivität Begehung'
    
    id = fields.Char(string='Identifikation')
    sequence_b = fields.Integer(string='Sequenz')
    nummer_eins = fields.Float(string="Nummer.")
    name = fields.Char(string="Name")
    klasse = fields.Selection([('klasse_1', 'Verkehrswege, Flucht- und Rettungswege'),
                               ('klasse_2', 'Beleuchtung, Lüftungs-, Heizeinrichtungen'),
                               ('klasse_3', 'Lagerung'),
                               ('klasse_4', 'Gefahrenhinweise'),
                               ('klasse_5', 'Arbeitsplatzgestaltung'),
                               ('klasse_6', 'Maschinen, Geräte, Betriebsmittel, Anlagen, Transportmittel, Bildschirm etc.'),
                               ('klasse_7', 'Aufbewahrung von chemischen Stoffen'),
                               ('klasse_8', 'Persönliche Schutzausrüstungen'),
                               ('klasse_9', 'Sicherheitseinrichtungen'),
                               ('klasse_10', 'Betriebsanweisungen'),
                               ('klasse_11', 'Erste-Hilfe- und Feuerlöscheinrichtungen')], 
                                string='Klassifizierung')
    abstellmassnahme = fields.Text(string="Abstellmaßnahme")
    abstellmassnahme_k = fields.Selection([('massnahme_k_1', ' Gefahrenquelle vermeiden / beseitigen (AAA)'),
                                           ('massnahme_k_2', 'Sicherheitstechnische Maßnahmen (AA)'),
                                           ('massnahme_k_3', 'Organisatorische Maßnahmen (A)'),
                                           ('massnahme_k_4', 'Nutzung PSA (BBB)'),
                                           ('massnahme_k_5', 'Verhaltensbezogene Maßnahmen (BB)')], 
                                            string='Abs Klassifizierung')
    
class BegehungZwei(models.Model):
    _name = 'begehung_zwei'
    _description = 'Aktivität Begehung zwei'

    id_zwei = fields.Char(string='Identifikation')
    sequence_b_zwei = fields.Integer(string='Sequenz z')
    nummer_zwei = fields.Float(string="Nr.")
    name_zwei = fields.Text(string="Name")
    klasse_zwei = fields.Selection([('klasse_1', 'Verkehrswege, Flucht- und Rettungswege'),
                                   ('klasse_2', 'Beleuchtung, Lüftungs-, Heizeinrichtungen'),
                                   ('klasse_3', 'Lagerung'),
                                   ('klasse_4', 'Gefahrenhinweise'),
                                   ('klasse_5', 'Arbeitsplatzgestaltung'),
                                   ('klasse_6', 'Maschinen, Geräte, Betriebsmittel, Anlagen, Transportmittel, Bildschirm etc.'),
                                   ('klasse_7', 'Aufbewahrung von chemischen Stoffen'),
                                   ('klasse_8', 'Persönliche Schutzausrüstungen'),
                                   ('klasse_9', 'Sicherheitseinrichtungen'),
                                   ('klasse_10', 'Betriebsanweisungen'),
                                   ('klasse_11', 'Erste-Hilfe- und Feuerlöscheinrichtungen')], 
                                    string='Klassifizierung')
    abstellmassnahme_zwei = fields.Text(string="Abstellmaßnahme", compute="")
    abstellmassnahme_k_zwei = fields.Selection([('massnahme_k_1', ' Gefahrenquelle vermeiden / beseitigen (AAA)'),
                                               ('massnahme_k_2', 'Sicherheitstechnische Maßnahmen (AA)'),
                                               ('massnahme_k_3', 'Organisatorische Maßnahmen (A)'),
                                               ('massnahme_k_4', 'Nutzung PSA (BBB)'),
                                               ('massnahme_k_5', 'Verhaltensbezogene Maßnahmen (BB)')], 
                                            string='Abs Klassifizierung')
    deadline_abs = fields.Date(string='Deadline Abstellmaßnahme')
    verantwortlich = fields.Many2one('res.partner', string='Verantwortlich')
    folg_erf =fields.Selection([('ja', 'Ja'),
                               ('nein', 'Nein')],
                              string='Folgebegehung erforderlich?')
    
    nummer_drei = fields.Float(string="Nummer.")
    name_drei = fields.Text(string="Name d")
    klasse_drei = fields.Selection([('klasse_3_1', 'Verkehrswege, Flucht- und Rettungswege'),
                                   ('klasse_3_2', 'Beleuchtung, Lüftungs-, Heizeinrichtungen'),
                                   ('klasse_3_3', 'Lagerung'),
                                   ('klasse_3_4', 'Gefahrenhinweise'),
                                   ('klasse_3_5', 'Arbeitsplatzgestaltung'),
                                   ('klasse_3_6', 'Maschinen, Geräte, Betriebsmittel, Anlagen, Transportmittel, Bildschirm etc.'),
                                   ('klasse_3_7', 'Aufbewahrung von chemischen Stoffen'),
                                   ('klasse_3_8', 'Persönliche Schutzausrüstungen'),
                                   ('klasse_3_9', 'Sicherheitseinrichtungen'),
                                   ('klasse_3_10', 'Betriebsanweisungen'),
                                   ('klasse_3_11', 'Erste-Hilfe- und Feuerlöscheinrichtungen')], 
                                    string='Klassifizierung')
    abstellmassnahme_drei = fields.Text(string="Abstellmaßnahme", compute="")
    abstellmassnahme_k_drei = fields.Selection([('massnahme_k_3_1', ' Gefahrenquelle vermeiden / beseitigen (AAA)'),
                                               ('massnahme_k_3_2', 'Sicherheitstechnische Maßnahmen (AA)'),
                                               ('massnahme_k_3_3', 'Organisatorische Maßnahmen (A)'),
                                               ('massnahme_k_3_4', 'Nutzung PSA (BBB)'),
                                               ('massnahme_k_3_5', 'Verhaltensbezogene Maßnahmen (BB)')], 
                                            string='Abs Klassifizierung')