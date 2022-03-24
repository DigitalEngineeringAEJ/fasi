# -*- coding: utf-8 -*-

import base64
from odoo import api, fields, models, _
from dateutil.relativedelta import relativedelta
from datetime import date
from odoo.exceptions import ValidationError
from collections import defaultdict
import calendar

class HazardTypes(models.Model):
    _name = 'hazard.types'
    _description = 'Hazard Types'
    _order = "sequence_g"

    name = fields.Char(string='Name')
    
    id = fields.Integer(string='ID')
    
    types_sn = fields.Char(string="S/N")
    
    gefaehrdungsf_name = fields.Many2one('gefahren.faktor', string="Gefährdungsfaktor")
    
    gefahrenquellen_typ_id = fields.Many2one('hazard.types', string="Gefährdungsfaktor Gruppe")
    
    gefahrenquellen_typ_beschreibung = fields.Text(string="Beschreibung")
    
    gefahrenquellen_typ_risiko = fields.Selection([('status_r_0', ''),
                                                   ('status_r_1', 'gering'), 
                                                   ('status_r_2', 'signifikant'),
                                                   ('status_r_3', 'hoch')],
                                                   string="Risiko", compute="_compute_typ_risiko", store=True)
    
    gefahrenquellen_typ_beschreibung_risikominderung = fields.Selection([('status_b_0', ''),
                                                                         ('status_b_1', 'Risiko akzeptabel'), 
                                                                         ('status_b_2', 'Reduzierung des Risikos notwendig'),
                                                                         ('status_b_3', 'Risiko-\nreduzierung dringend erforderlich')],
                                                                        string="Beschreibung/Risikominderung", compute="_compute_beschreibung_risikominderung", store=True)
    

    gef_beurteilung_w = fields.Selection([('status_w_1', 'sehr gering'), 
                                          ('status_w_2', 'gering'),
                                          ('status_w_3', 'mittel'),
                                          ('status_w_4', 'hoch')], 
                                         string='Eintrittswahrscheinlichkeit')
    
    gef_beurteilung_a = fields.Selection([('status_a_1', 'leichte Verletzugen oder Erkrankungen'),
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
                               ('Beleuchtung, Lüftungs-, Heiz-\neinrichtungen', 'Beleuchtung, Lüftungs-, Heizeinrichtungen'),
                               ('Lagerung', 'Lagerung'),
                               ('Gefahren-\nhinweise', 'Gefahrenhinweise'),
                               ('Arbeitsplatz-\ngestaltung', 'Arbeitsplatzgestaltung'),
                               ('Maschinen, Geräte, Betriebsmittel, Anlagen, Transportmittel, Bildschirm etc.', 'Maschinen, Geräte, Betriebsmittel, Anlagen, Transportmittel, Bildschirm etc.'),
                               ('Aufbewahrung von chemischen Stoffen', 'Aufbewahrung von chemischen Stoffen'),
                               ('Persönliche Schutz\nausrüstungen', 'Persönliche Schutzausrüstungen'),
                               ('Sicherheits-\neinrichtungen', 'Sicherheitseinrichtungen'),
                               ('Betriebsan-\nweisungen', 'Betriebsanweisungen'),
                               ('Erste-Hilfe- und Feuerlösch-\neinrichtungen', 'Erste-Hilfe- und Feuerlöscheinrichtungen')], 
                                string='Klassifizierung')
    
    
    abstellmassnahme_gef_kla = fields.Selection([('Gefahrenquelle vermeiden / beseitigen (AAA)', 'Gefahrenquelle vermeiden / beseitigen (AAA)'),
                                           ('Sicherheitstechnische Maßnahmen (AA)', 'Sicherheitstechnische Maßnahmen (AA)'),
                                           ('Organisatorische Maßnahmen (A)', 'Organisatorische Maßnahmen (A)'),
                                           ('Nutzung PSA (BBB)', 'Nutzung PSA (BBB)'),
                                           ('Verhaltensbezogene Maßnahmen (BB)', 'Verhaltensbezogene Maßnahmen (BB)')], 
                                            string='Abs Klassifizierung')
    abs_gef = fields.Char(string="Abstellmaßnahme")
    
    deadline_abs_gef = fields.Date(string='Deadline Abstellmaßnahme')
    
    customer_id = fields.Many2one('res.partner', string='Veranwortlich')
    
    folg_beg_gef =fields.Selection([('Ja', 'Ja'),
                               ('Nein', 'Nein')],
                              string='Folgebegehung erforderlich?', default='Nein')
    
    equipment_protocol_id = fields.Many2one('hazard.protocol')
    
    nummer_gef = fields.Char(string="Nummer", compute="_compute_nummer_gef", store=1)
    
    equipment_id = fields.Many2one('safety.master', string='Equipment', store=True)
    

    
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
    @api.model
    def create(self, vals):
        result = super(HazardTypes, self).create(vals)
        if result.name:
            gefaehrdunsfaktors = self.env['hazard.types'].search([('name', '=', result.name)])
        else:
            gefaehrdunsfaktors= self.env['hazard.types'].search([('mail_activity_id', '=', result.id)])
        if not len(gefaehrdunsfaktors):
            result.sequence_g = result.sequence_g+1
        elif len(gefaehrdunsfaktors)==1:
            result.sequence_g = gefaehrdunsfaktors[-1].sequence_g + 1
        else:
            result.sequence_g = gefaehrdunsfaktors[-2].sequence_g +1
        return result
    
    @api.depends('sequence_g')
    def _compute_nummer_gef(self):
        """compute sequence_g."""
        for rec in self:
            if rec.sequence_g:
                rec.nummer_gef = "1." + ("0"+ str(rec.sequence_g)) if len(str(rec.sequence_g)) == 1 else "1." +str(rec.sequence_g)
                
                
#     @api.depends('equipment_id')
#     def _get_customer(self):
#         for activity in self:
#             activity.customer_id = activity.equipment_id.customer_id if activity else False
            
#     def _inverse_customer(self):
#         for customer in self:
#             customer.customer_id.name = customer.name


                
class GefahrenFaktor(models.Model):
    _name = 'gefahren.faktor'
    _description = 'Gefährdungsfaktor'
    _rec_name = 'gefaehrdungsf'
    
    gefaehrdungsf = fields.Char(string='Gefährdungsfaktoren')
    gefahrenquellen_typ_id = fields.Many2one('hazard.types', string="Gefährdungsfaktor Gruppe")