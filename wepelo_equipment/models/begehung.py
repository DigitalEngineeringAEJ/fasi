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
    nummer_eins = fields.Char(string="Nummer",  store=True, readonly=True)
    name = fields.Char(string="Name")
    name_eins = fields.Char(string="Name")
    klasse = fields.Selection([('Verkehrswege, Flucht- und Rettungswege', 'Verkehrswege, Flucht- und Rettungswege'),
                               ('Beleuchtung, Lüftungs-, Heizeinrichtungen', 'Beleuchtung, Lüftungs-, Heizeinrichtungen'),
                               ('Lagerung', 'Lagerung'),
                               ('Gefahrenhinweise', 'Gefahrenhinweise'),
                               ('Arbeitsplatzgestaltung', 'Arbeitsplatzgestaltung'),
                               ('Maschinen, Geräte, Betriebsmittel, Anlagen, Transportmittel, Bildschirm etc.', 'Maschinen, Geräte, Betriebsmittel, Anlagen, Transportmittel, Bildschirm etc.'),
                               ('Aufbewahrung von chemischen Stoffen', 'Aufbewahrung von chemischen Stoffen'),
                               ('Persönliche Schutzausrüstungen', 'Persönliche Schutzausrüstungen'),
                               ('Sicherheitseinrichtungen', 'Sicherheitseinrichtungen'),
                               ('Betriebsanweisungen', 'Betriebsanweisungen'),
                               ('Erste-Hilfe- und Feuerlöscheinrichtungen', 'Erste-Hilfe- und Feuerlöscheinrichtungen')], 
                                string='Klassifizierung')
    abstellmassnahme = fields.Text(string="Abstellmaßnahme")
    abstellmassnahme_k = fields.Selection([('Gefahrenquelle vermeiden / beseitigen (AAA)', 'Gefahrenquelle vermeiden / beseitigen (AAA)'),
                                           ('Sicherheitstechnische Maßnahmen (AA)', 'Sicherheitstechnische Maßnahmen (AA)'),
                                           ('Organisatorische Maßnahmen (A)', 'Organisatorische Maßnahmen (A)'),
                                           ('Nutzung PSA (BBB)', 'Nutzung PSA (BBB)'),
                                           ('Verhaltensbezogene Maßnahmen (BB)', 'Verhaltensbezogene Maßnahmen (BB)')], 
                                            string='Abs Klassifizierung')
    relationm = fields.Many2one('mail.activity')
    relatione = fields.Many2one('equipment.protocol')
    
    @api.model
    def create(self, vals):
        if vals.get('nummer_eins', 'New') == 'New':
            vals['nummer_eins'] = self.env['ir.sequence'].next_by_code('begehung.eins') or 'New'
        result = super(Begehung, self).create(vals)
        return result
    
class BegehungZwei(models.Model):
    _name = 'begehung_zwei'
    _description = 'Aktivität Begehung zwei'

    id_zwei = fields.Char(string='Identifikation')
    
    sequence_b_zwei = fields.Integer(string='Sequenz z')
    
    nummer_zwei = fields.Float(string="Nr.")
    
    name_zwei = fields.Text(string="Name")
    
    klasse_zwei =fields.Selection([('Verkehrswege, Flucht- und Rettungswege', 'Verkehrswege, Flucht- und Rettungswege'),
                               ('Beleuchtung, Lüftungs-, Heizeinrichtungen', 'Beleuchtung, Lüftungs-, Heizeinrichtungen'),
                               ('Lagerung', 'Lagerung'),
                               ('Gefahrenhinweise', 'Gefahrenhinweise'),
                               ('Arbeitsplatzgestaltung', 'Arbeitsplatzgestaltung'),
                               ('Maschinen, Geräte, Betriebsmittel, Anlagen, Transportmittel, Bildschirm etc.', 'Maschinen, Geräte, Betriebsmittel, Anlagen, Transportmittel, Bildschirm etc.'),
                               ('Aufbewahrung von chemischen Stoffen', 'Aufbewahrung von chemischen Stoffen'),
                               ('Persönliche Schutzausrüstungen', 'Persönliche Schutzausrüstungen'),
                               ('Sicherheitseinrichtungen', 'Sicherheitseinrichtungen'),
                               ('Betriebsanweisungen', 'Betriebsanweisungen'),
                               ('Erste-Hilfe- und Feuerlöscheinrichtungen', 'Erste-Hilfe- und Feuerlöscheinrichtungen')], 
                                string='Klassifizierung')
    
    abstellmassnahme_zwei = fields.Text(string="Abstellmaßnahme", compute="")
    
    abstellmassnahme_k_zwei = fields.Selection([('Gefahrenquelle vermeiden / beseitigen (AAA)', 'Gefahrenquelle vermeiden / beseitigen (AAA)'),
                                           ('Sicherheitstechnische Maßnahmen (AA)', 'Sicherheitstechnische Maßnahmen (AA)'),
                                           ('Organisatorische Maßnahmen (A)', 'Organisatorische Maßnahmen (A)'),
                                           ('Nutzung PSA (BBB)', 'Nutzung PSA (BBB)'),
                                           ('Verhaltensbezogene Maßnahmen (BB)', 'Verhaltensbezogene Maßnahmen (BB)')], 
                                            string='Abs Klassifizierung')
    
    deadline_abs = fields.Date(string='Deadline Abstellmaßnahme')
    
    verantwortlich = fields.Many2one('res.partner', string='Verantwortlich')
    
    folg_erf_m =fields.Selection([('Ja', 'Ja'),
                               ('Nein', 'Nein')],
                              string='Folgebegehung erforderlich?')
    
    nummer_drei = fields.Char(string="Nummer",  store=True, readonly=True)
    
    name_drei = fields.Text(string="Name")
    
    
    relation_m = fields.Many2one('mail.activity')
    relation_e = fields.Many2one('equipment.protocol')
    
    relation_f = fields.Many2one('folgebegehung')
    
    @api.model
    def create(self, vals):
        if vals.get('nummer_drei', 'New') == 'New':
            vals['nummer_drei'] = self.env['ir.sequence'].next_by_code('begehung.zwei') or 'New'
        result = super(BegehungZwei, self).create(vals)
        return result
    
class Folgebegehung(models.Model):
    _name = 'folgebegehung'
    _description = 'Aktivität Folgebegehung'
    
    mail_id = fields.Many2one('mail.activity')
    protocol_id = fields.Many2one('equipment.protocol')
    begehungs_id = fields.Many2one('begehung')
    begehungs_id_zwei = fields.Many2one('begehung_zwei')
    
    id_ref = fields.Char(string='Identifikation')
    
    sequence_ref= fields.Integer(string='Sequenz z')
    
    nummer_vier = fields.Float(string='Nr')
    
    name_vier = fields.Text(string='Name')
    
    klasse_drei = fields.Char(string='Klassifizierung')
    
    abstellmassnahme_drei = fields.Text(string="Abstellmaßnahme",)
    
    abstellmassnahme_k_drei = fields.Char(string='Abs Klassifizierung')
    
    deadline_abs_ref = fields.Date(string='Deadline Abstellmaßnahme')
    
    verantwortlich_ref = fields.Many2one('res.partner', string='Verantwortlich')
    
    wirksam =fields.Selection([('Ja', 'Ja'),
                               ('Nein', 'Nein')],
                              string='Maßnahmen wirksam?')
    
    w_folg_erf =fields.Selection([('Ja', 'Ja'),
                               ('Nein', 'Nein')],
                              string='Folgebegehung erforderlich?')
    