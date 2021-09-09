# -*- coding: utf-8 -*-

import base64
from odoo import api, fields, models, _
from dateutil.relativedelta import relativedelta
from datetime import date
from odoo.exceptions import ValidationError
from collections import defaultdict
import calendar

class EquipmentTypes(models.Model):
    _name = 'equipment.types'
    _description = 'Equipment Types'

    name = fields.Char(string='Name')
    
    id = fields.Integer(string='ID')
    
    types_sn = fields.Char(string="S/N")
    
    gefaehrdungsf_name = fields.Many2one('gefahren.faktor', string="Gefährdungsfaktor")
    
    sequence_g = fields.Integer(string='Sequenz')
    
    gefahrenquellen_typ_id = fields.Many2one('equipment.types', string="Gefährdungsfaktor Gruppe") 
    
    gefahrenquellen_typ_beschreibung = fields.Text(string="Beschreibung")
    
    gefahrenquellen_typ_risiko = fields.Selection([('status_r_0', ''),
                                                   ('status_r_1', 'gering'), 
                                                   ('status_r_2', 'signifikant'),
                                                   ('status_r_3', 'hoch')],
                                                   string="Risiko", compute="_compute_typ_risiko", store=True)
    
    gefahrenquellen_typ_beschreibung_risikominderung = fields.Selection([('status_b_0', ''),
                                                                         ('status_b_1', 'Risiko akzeptabel'), 
                                                                         ('status_b_2', 'Reduzierung des Risikos notwendig'),
                                                                         ('status_b_3', 'Risikoreduzierung dringend erforderlich')],
                                                                        string="Beschreibung/Risikominderung", compute="_compute_beschreibung_risikominderung", store=True)
    

    gef_beurteilung_w = fields.Selection([('status_w_1', 'sehr gering'), 
                                          ('status_w_2', 'gering'),
                                          ('status_w_3', 'mittel'),
                                          ('status_w_4', 'hoch')], 
                                         string='Eintrittswahrscheinlichkeit')
    
    gef_beurteilung_a = fields.Selection([('status_a_1', 'leichte Verletzugen oder Erkrankugen'),
                                          ('status_a_2', 'mittelschwere Verletzungen oder Erkrankungen'),
                                          ('status_a_3', 'schwere Verletzungen oder Erkrankungen'),
                                          ('status_a_4', 'möglicher Tod, Katastrophe')], 
                                         string='Ausmaß')
    
    gef_beurteilung_e = fields.Selection([('status_e_0', '0'),
                                          ('status_e_1', '1'),
                                          ('status_e_2', '2'),
                                          ('status_e_3', '3'),
                                          ('status_e_4', '4'),
                                          ('status_e_5', '5'),
                                          ('status_e_6', '6'),
                                          ('status_e_7', '7')], 
                                         string='Maßzahl', compute="_compute_gef_beurteilung_e", store=True)
    mail_activity_id =  fields.Many2one('mail.activity', string="Mail Activity")
    
    
    sequence_g = fields.Integer(string='Sequenz')
    
    gefaehrdungsf_id = fields.One2many('gefahren.faktor', 'gefaehrdungsf')
    
    klasse_gef =fields.Selection([('Verkehrswege, Flucht- und Rettungswege', 'Verkehrswege, Flucht- und Rettungswege'),
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
    
    abstellmassnahme_gef = fields.Text(string="Abstellmaßnahme", compute="")
    
    abstellmassnahme_gef = fields.Selection([('Gefahrenquelle vermeiden / beseitigen (AAA)', 'Gefahrenquelle vermeiden / beseitigen (AAA)'),
                                           ('Sicherheitstechnische Maßnahmen (AA)', 'Sicherheitstechnische Maßnahmen (AA)'),
                                           ('Organisatorische Maßnahmen (A)', 'Organisatorische Maßnahmen (A)'),
                                           ('Nutzung PSA (BBB)', 'Nutzung PSA (BBB)'),
                                           ('Verhaltensbezogene Maßnahmen (BB)', 'Verhaltensbezogene Maßnahmen (BB)')], 
                                            string='Abs Klassifizierung')
    
    deadline_abs_gef = fields.Date(string='Deadline Abstellmaßnahme')
    
    verantwortlich_gef = fields.Many2one('res.partner', string='Verantwortlich')
    
    folg_beg_gef =fields.Selection([('Ja', 'Ja'),
                               ('Nein', 'Nein')],
                              string='Folgebegehung erforderlich?')
    
    @api.depends('gef_beurteilung_w', 'gef_beurteilung_a')
    def _compute_gef_beurteilung_e(self):
        for record in self:
            if record.gef_beurteilung_w == 'status_w_1' and record.gef_beurteilung_a == 'status_a_1':
                record.gef_beurteilung_e = 'status_e_1' 
                
            elif record.gef_beurteilung_w == 'status_w_1' and record.gef_beurteilung_a == 'status_a_2':
                record.gef_beurteilung_e = 'status_e_2' 
                
            elif record.gef_beurteilung_w == 'status_w_1' and record.gef_beurteilung_a == 'status_a_3':
                record.gef_beurteilung_e = 'status_e_3' 
                
            elif record.gef_beurteilung_w == 'status_w_1' and record.gef_beurteilung_a == 'status_a_4':
                record.gef_beurteilung_e = 'status_e_4' 
                
            elif record.gef_beurteilung_w == 'status_w_2' and record.gef_beurteilung_a == 'status_a_1':
                record.gef_beurteilung_e = 'status_e_2' 
                
            elif record.gef_beurteilung_w == 'status_w_2' and record.gef_beurteilung_a == 'status_a_2':
                record.gef_beurteilung_e = 'status_e_3'
                
            elif record.gef_beurteilung_w == 'status_w_2' and record.gef_beurteilung_a == 'status_a_3':
                record.gef_beurteilung_e = 'status_e_4' 
                
            elif record.gef_beurteilung_w == 'status_w_2' and record.gef_beurteilung_a == 'status_a_4':
                record.gef_beurteilung_e = 'status_e_5' 
                
            elif record.gef_beurteilung_w == 'status_w_3' and record.gef_beurteilung_a == 'status_a_1':
                record.gef_beurteilung_e = 'status_e_3' 
                
            elif record.gef_beurteilung_w == 'status_w_3' and record.gef_beurteilung_a == 'status_a_2':
                record.gef_beurteilung_e = 'status_e_4' 
                
            elif record.gef_beurteilung_w == 'status_w_3' and record.gef_beurteilung_a == 'status_a_3':
                record.gef_beurteilung_e = 'status_e_5' 
                
            elif record.gef_beurteilung_w == 'status_w_3' and record.gef_beurteilung_a == 'status_a_4':
                record.gef_beurteilung_e = 'status_e_6'
                
            elif record.gef_beurteilung_w == 'status_w_4' and record.gef_beurteilung_a == 'status_a_1':
                record.gef_beurteilung_e = 'status_e_4' 
                
            elif record.gef_beurteilung_w == 'status_w_4' and record.gef_beurteilung_a == 'status_a_2':
                record.gef_beurteilung_e = 'status_e_5' 
                
            elif record.gef_beurteilung_w == 'status_w_4' and record.gef_beurteilung_a == 'status_a_3':
                record.gef_beurteilung_e = 'status_e_6' 
                
            elif record.gef_beurteilung_w == 'status_w_4' and record.gef_beurteilung_a == 'status_a_4':
                record.gef_beurteilung_e = 'status_e_7' 
                
            else:
                record.gef_beurteilung_e = 'status_e_0'
                
    @api.depends('gef_beurteilung_e')
    def _compute_beschreibung_risikominderung(self):
        for record in self:
            if record.gef_beurteilung_e == 'status_e_1':
                record.gefahrenquellen_typ_beschreibung_risikominderung = 'status_b_1'
            elif record.gef_beurteilung_e == 'status_e_2':
                record.gefahrenquellen_typ_beschreibung_risikominderung = 'status_b_1'
            elif record.gef_beurteilung_e == 'status_e_3':
                record.gefahrenquellen_typ_beschreibung_risikominderung = 'status_b_2'
            elif record.gef_beurteilung_e == 'status_e_4':
                record.gefahrenquellen_typ_beschreibung_risikominderung = 'status_b_2'
            elif record.gef_beurteilung_e == 'status_e_5':
                record.gefahrenquellen_typ_beschreibung_risikominderung = 'status_b_3'
            elif record.gef_beurteilung_e == 'status_e_6':
                record.gefahrenquellen_typ_beschreibung_risikominderung = 'status_b_3'
            elif record.gef_beurteilung_e == 'status_e_7':
                record.gefahrenquellen_typ_beschreibung_risikominderung = 'status_b_3'
            else:
                record.gefahrenquellen_typ_beschreibung_risikominderung = 'status_b_0'
                
    @api.depends('gef_beurteilung_e')
    def _compute_typ_risiko(self):
        for record in self:
            if record.gef_beurteilung_e == 'status_e_1':
                record.gefahrenquellen_typ_risiko = 'status_r_1'
            elif record.gef_beurteilung_e == 'status_e_2':
                record.gefahrenquellen_typ_risiko = 'status_r_1'
            elif record.gef_beurteilung_e == 'status_e_3':
                record.gefahrenquellen_typ_risiko = 'status_r_2'
            elif record.gef_beurteilung_e == 'status_e_4':
                record.gefahrenquellen_typ_risiko = 'status_r_2'
            elif record.gef_beurteilung_e == 'status_e_5':
                record.gefahrenquellen_typ_risiko = 'status_r_3'
            elif record.gef_beurteilung_e == 'status_e_6':
                record.gefahrenquellen_typ_risiko = 'status_r_3'
            elif record.gef_beurteilung_e == 'status_e_7':
                record.gefahrenquellen_typ_risiko = 'status_r_3'
            else:
                record.gefahrenquellen_typ_risiko = 'status_r_0'
                
                
class EquipmentTypes(models.Model):
    _name = 'gefahren.faktor'
    _description = 'Gefährdungsfaktor'
    _rec_name = 'gefaehrdungsf'
    
    gefaehrdungsf = fields.Char(string='Gefährdungsfaktoren')
    gefahrenquellen_typ_id = fields.Many2one('equipment.types', string="Gefährdungsfaktor Gruppe")