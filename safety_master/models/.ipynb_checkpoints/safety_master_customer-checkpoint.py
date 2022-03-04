# -*- coding: utf-8 -*-
# wepelo_customer.py

from odoo import api, fields, models, _

# Anlage der Felder für das 
class customerPartner(models.Model):
    _inherit = 'res.partner'
    
    contact_person =fields.Char(string="txtt")
    additive = fields.Char(string='Txt')
    zip = fields.Char(string='Zip')
    zip2 = fields.Char(string='Zip2', compute='_compute_two_zip')
    
    def _compute_two_zip(self):
        if self.zip:
            self.zip2 = self.zip[:2]
    
    @api.onchange('city')
    def onchange_city_country(self):
        if self.city:
            self.country_id = 57


# class IrAttachment(models.Model):
#     _inherit = 'ir.attachment'
#     _order='create_date'
