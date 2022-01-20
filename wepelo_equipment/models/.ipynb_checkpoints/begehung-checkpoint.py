# -*- coding: utf-8 -*-

import base64
from odoo import api, fields, models, _
from dateutil.relativedelta import relativedelta
from datetime import date
from odoo.exceptions import ValidationError
from collections import defaultdict
import calendar
#
class Begehung(models.Model):
    _name = 'begehung'
    _description = 'Aktivität Begehung'
    _order = "sequence_b"
    
    id = fields.Char(string='Identifikation')
    sequence_b = fields.Integer(string='Sequenz')
    nummer_eins = fields.Char(string="Nummer", compute="_compute_nummer_eins", store=1)
    name = fields.Char(string="Name.")
    name_eins = fields.Char(string="Nam.")
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
        result = super(Begehung, self).create(vals)
        if result.name:
            begehung = self.env['begehung'].search([('name', '=', result.name)])
        else:
            begehung= self.env['begehung'].search([('relationm', '=', result.id)])
        if not len(begehung):
            result.sequence_b = result.sequence_b+1
        elif len(begehung)==1:
            result.sequence_b = begehung[-1].sequence_b + 1
        else:
            result.sequence_b = begehung[-2].sequence_b +1
        return result
    
    @api.depends('sequence_b')
    def _compute_nummer_eins(self):
        """compute sequence_b."""
        for rec in self:
            if rec.sequence_b:
                rec.nummer_eins = "1." + ("0"+ str(rec.sequence_b)) if len(str(rec.sequence_b)) == 1 else "1." +str(rec.sequence_b)

    

    
class BegehungZwei(models.Model):
    _name = 'begehung_zwei'
    _description = 'Aktivität Begehung zwei'
    _order = "sequence_b_zwei"

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
    
    abstellmassnahme_zwei = fields.Text(string="Abstellmaßnahme")
    
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
                              string='Folgebegehung erforderlich?', default='Nein')
    
    nummer_drei = fields.Char(string="Nummer", compute="_compute_nummer_zwei", store=1)
    
    name_drei = fields.Text(string="Name.")
    
    
    relation_m = fields.Many2one('mail.activity')
    relation_e = fields.Many2one('equipment.protocol')
        
        
    @api.model
    def create(self, vals):
        result = super(BegehungZwei, self).create(vals)
        if result.name_zwei:
            begehungzwei = self.env['begehung_zwei'].search([('name_zwei', '=', result.name_zwei)])
        else:
            begehungzwei= self.env['begehung_zwei'].search([('relation_m', '=', result.id)])
        if not len(begehungzwei):
            result.sequence_b_zwei = result.sequence_b_zwei+1
        elif len(begehungzwei)==1:
            result.sequence_b_zwei = begehungzwei[-1].sequence_b_zwei + 1
        else:
            result.sequence_b_zwei = begehungzwei[-2].sequence_b_zwei +1
        return result
    
    @api.depends('sequence_b_zwei')
    def _compute_nummer_zwei(self):
        """compute sequence_b_zwei."""
        for rec in self:
            if rec.sequence_b_zwei:
                rec.nummer_drei = "1." + ("0"+ str(rec.sequence_b_zwei)) if len(str(rec.sequence_b_zwei)) == 1 else "1." +str(rec.sequence_b_zwei)

    
class Folgebegehung(models.Model):
    _name = 'folgebegehung'
    _description = 'Aktivität Folgebegehung'
    
    mail_id = fields.Many2one('mail.activity')
    
    protocol_id = fields.Many2one('equipment.protocol')
    
    begehungs_id = fields.Many2one('begehung')
    
    begehungs_id_zwei = fields.Many2one('begehung_zwei')
    
    id_ref = fields.Char(string='Identifikation')
    
    sequence_ref= fields.Integer(string='Sequenz z')
    
    nummer_vier =fields.Char(string="Nummer", compute="_compute_nummer_vier", store=1)
    
    name_vier = fields.Text(string='Name')
    
    klasse_drei = fields.Selection([('Verkehrswege, Flucht- und Rettungswege', 'Verkehrswege, Flucht- und Rettungswege'),
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
    
    abstellmassnahme_drei = fields.Text(string="Abstellmaßnahme",)
    
    abstellmassnahme_k_drei = fields.Selection([('Gefahrenquelle vermeiden / beseitigen (AAA)', 'Gefahrenquelle vermeiden / beseitigen (AAA)'),
                                           ('Sicherheitstechnische Maßnahmen (AA)', 'Sicherheitstechnische Maßnahmen (AA)'),
                                           ('Organisatorische Maßnahmen (A)', 'Organisatorische Maßnahmen (A)'),
                                           ('Nutzung PSA (BBB)', 'Nutzung PSA (BBB)'),
                                           ('Verhaltensbezogene Maßnahmen (BB)', 'Verhaltensbezogene Maßnahmen (BB)')], 
                                            string='Abs Klassifizierung')
    
    deadline_abs_ref = fields.Date(string='Deadline Abstellmaßnahme')
    
    verantwortlich_ref = fields.Many2one('res.partner', string='Verantwortlich')
    
    wirksam =fields.Selection([('Ja', 'Ja'),
                               ('Nein', 'Nein')],
                              string='Maßnahmen wirksam?')
    
    w_folg_erf =fields.Selection([('Ja', 'Ja'),
                               ('Nein', 'Nein')],
                              string='Folgebegehung erforderlich?', default='Nein')
    
    @api.model
    def create(self, vals):
        result = super(Folgebegehung, self).create(vals)
        if result.name_vier:
            folgebegehung = self.env['folgebegehung'].search([('name_vier', '=', result.name_vier)])
        else:
            folgebegehung= self.env['folgebegehung'].search([('mail_id', '=', result.id)])
        if not len(folgebegehung):
            result.sequence_ref = result.sequence_ref+1
        elif len(folgebegehung)==1:
            result.sequence_ref = folgebegehung[-1].sequence_ref + 1
        else:
            result.sequence_ref = folgebegehung[-2].sequence_ref +1
        return result
    
    @api.depends('sequence_ref')
    def _compute_nummer_vier(self):
        """compute sequence_ref."""
        for rec in self:
            if rec.sequence_ref:
                rec.nummer_vier = "1." + ("0"+ str(rec.sequence_ref)) if len(str(rec.sequence_ref)) == 1 else "1." +str(rec.sequence_ref)
    