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
    
    types_sn = fields.Char(string="S/N")
    
    sequence_g = fields.Integer(string='Sequenz')
    
    gefahrenquellen_typ_id = fields.Many2one('equipment.types', string="Gefährdungsfaktor Gruppe")
    
    gefahrenquellen_typ_beschreibung = fields.Text(string="Beschreibung")
    
    gefahrenquellen_typ_risiko = fields.Text(string="Risiko")
    
    gefahrenquellen_typ_beschreibung_risikominderung = fields.Text(string="Beschreibung/Risikominderung")
    
#     check = fields.Boolean(compute='_dann_aktiv')

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
    
    gef_beurteilung_e = fields.Selection([('status_e_1', '1'),
                                          ('status_e_2', '2'),
                                          ('status_e_3', '3'),
                                          ('status_e_4', '4'),
                                          ('status_e_5', '5'),
                                          ('status_e_6', '6'),
                                          ('status_e_7', '7')], 
                                         string='Maßzahl')
    
    sequence_g = fields.Integer(string='Sequenz')
    
#     @api.onchange('gef_beurteilung_w', 'gef_beurteilung_a', 'gef_beurteilung_e') 
#     def onchange__berechnung_mas(self):
#         for record in self:
#             if 'status_w_1' and 'status_a_1':
#                 return self.gef_beurteilung_e = 'status_e_1'
#             elif self.gef_beurteilung_w == 'status_w_1' and self.gef_beurteilung_a == 'status_a_2':
#                 return self.gef_beurteilung_e = 'status_e_2'
#             elif self.gef_beurteilung_w == 'status_w_1' and self.gef_beurteilung_a =='status_a_3':
#                 return self.gef_beurteilung_e = 'status_e_3'
#             elif self.gef_beurteilung_w == 'status_w_1' and self.gef_beurteilung_a =='status_a_4':
#                 return self.gef_beurteilung_e = 'status_e_4'
#             elif self.gef_beurteilung_w == 'status_w_2' and self.gef_beurteilung_a =='status_a_1':
#                 return self.gef_beurteilung_e = 'status_e_2'
#             elif self.gef_beurteilung_w == 'status_w_2' and self.gef_beurteilung_a =='status_a_2':
#                 return self.gef_beurteilung_e = 'status_e_3'
#             elif self.gef_beurteilung_w == 'status_w_2' and self.gef_beurteilung_a =='status_a_3':
#                 return self.gef_beurteilung_e = 'status_e_4'
#             elif self.gef_beurteilung_w == 'status_w_2' and self.gef_beurteilung_a =='status_a_4':
#                 return self.gef_beurteilung_e = 'status_e_5'
#             elif self.gef_beurteilung_w == 'status_w_3' and self.gef_beurteilung_a =='status_a_1':
#                 return self.gef_beurteilung_e = 'status_e_3'
#             elif self.gef_beurteilung_w == 'status_w_3' and self.gef_beurteilung_a =='status_a_2':
#                 return self.gef_beurteilung_e = 'status_e_4'
#             elif self.gef_beurteilung_w == 'status_w_3' and self.gef_beurteilung_a =='status_a_3':
#                 return self.gef_beurteilung_e = 'status_e_5'
#             elif self.gef_beurteilung_w == 'status_w_3' and self.gef_beurteilung_a =='status_a_4':
#                 return self.gef_beurteilung_e = 'status_e_6'
#             elif self.gef_beurteilung_w == 'status_w_4' and self.gef_beurteilung_a =='status_a_1':
#                 return self.gef_beurteilung_e = 'status_e_4'
#             elif self.gef_beurteilung_w == 'status_w_4' and self.gef_beurteilung_a =='status_a_2':
#                 return self.gef_beurteilung_e = 'status_e_5'
#             elif self.gef_beurteilung_w == 'status_w_4' and self.gef_beurteilung_a =='status_a_3':
#                 return self.gef_beurteilung_e = 'status_e_6'
#             elif self.gef_beurteilung_w == 'status_w_4' and self.gef_beurteilung_a =='status_a_4':
#                 return self.gef_beurteilung_e = 'status_e_7'
#             else:
#                 return self.gef_beurteilung_e = ''