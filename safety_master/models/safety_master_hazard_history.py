# -*- coding: utf-8 -*-
# wepelo_history.py

from odoo import api, fields, models, _
import datetime

# Anlage der Felder 
class HazardHistory(models.Model):
    _name = 'hazard.history'
    _inherit = 'safety.master'
    _description ='Historie des Inventars'
    #_rec_name = 'name'
    #name = fields.Char(string='Equipment Name')
    #date_hist = fields
    namehist = fields.Char(string='Name History')
    current_date = fields.Datetime(string='My date')
    topic = fields.Char(string='Topic')
    name = fields.Many2one('safety.master', string='Equipment')
    request_id = fields.Many2one('hazard.request', string='Reparatur')