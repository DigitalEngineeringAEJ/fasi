# -*- coding: utf-8 -*-

import base64
from odoo import api, fields, models, _
from dateutil.relativedelta import relativedelta
from datetime import date
from odoo.exceptions import ValidationError
from collections import defaultdict
import calendar

class Unterweisung(models.Model):
    _name = 'unterweisung'
    _description = 'Unterweisung'

    name = fields.Char(string='Name')
    
    id = fields.Char(string='Identifikation')
    
    sequence = fields.Integer(string='Sequenz')
    
    name_customer = fields.Char(string='Unterschrift der Teilnehmer')
    
    signature_customer = fields.Binary(string='Signatur Teilnehmer')
    
    name_trainer = fields.Char(string='Unterschrift des Trainers')
    
    signature_trainer = fields.Binary(string='Signatur Trainer')

    
    
    
    