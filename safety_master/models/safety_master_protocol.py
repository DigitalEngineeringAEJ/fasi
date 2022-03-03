# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class HazardProtocol(models.Model):
    _name = 'hazard.protocol'
    _inherit = ['mail.thread', 'equipment.mail.activity']
    _description = 'Hazard Protocol'
    _rec_name = 'name'

    x_garantie = fields.Boolean(string='liegt eine Garantie vor')
    x_reparatur = fields.Text('Reparatur')
    x_durchPI = fields.Text('durch PI/Region')
    x_angegebener_fehler = fields.Text('angegebener Fehler')
    name = fields.Char(string="Name")
    order_date = fields.Date(string='Order Date')
    customer_id = fields.Many2one('res.partner', string='Customer')
    contractor_id = fields.Many2one('res.users', string='Contractor')
    testing_device = fields.Char(string='Testing Device')
    testing_device = fields.Char(string='Testing Device')
    testing_device_sn = fields.Char(string="S/N")
    manufacturer_id = fields.Many2one('res.partner', string='Manufacturer')
    equipment_id = fields.Many2one('safety.master', string='Gefahrenquelle')
    equipment_service_id = fields.Many2one('hazard.service', string='Equipment System')
    mail_activity_id = fields.Many2one('mail.activity', string='Mail Activity')
    equipment_test_type_id = fields.Many2one(related='mail_activity_id.equipment_test_type_id', store=True, readonly=True)
    equipment_test_type = fields.Selection([
        ('calibration_ei', _('Gefähdungsbeuteilung')),
        ('el_test', _('Folgebegehung')),
        ('routine_test', _('Begehung')),
        ('calibration', _('Betriebsanweisung Gefahrstoffe')),
        ('betriebsanweisung', _('Betriebsanweisung Maschinen und Arbeitsverfahren')),
        ('uvv', _('Betriebssicherheitsprüfung')),
        ('maintenance', _('Betriebsanweisung PSA')),
        ('repairs', _('Reparatur')),
        ('gefahrstoff_verszeichnis', _('Gefahrstoff-Verszeichnis')),
        ('unterweisung', _('Unterweisung')),
        ('el_pruefung_buero', _('Elektroprüfung Büro')),
        ('el_pruefung_werk_prod', _('Elektroprüfung Werkstatt/Produktion')),
        ('pruefung_fuerloescher', _('Prüfung Feuerlöscher')),
        ('bet_sich_pruefung', _('Betriebssicherheitsprüfung')),
    ], compute="_compute_equipment_test_type", string='Service')
    serial_no = fields.Char(string='Serial No')
    type = fields.Char(string='Type')
    sensor_type = fields.Char(string='Sensor Type')
    sensor_serial = fields.Char(string='Serial Number')
    gas_certificate_no = fields.Char(string='Certificate No')
    gas_bottle_no = fields.Char(string='Bottle No')
    remarks = fields.Char(string='Remarks')
    date = fields.Date(string='Due Date')
    #Anpassungen per 22.12.2020
    category_id = fields.Many2one(string='Category', related='equipment_id.category_id')
    description = fields.Char(string='Beschreibung Anmerkungen')
    #Anpassung per 26.12.2020
    ref = fields.Char(string='Kunden-Nummer')
    maintenance_request_id = fields.Many2one('hazard.request', string='Maintenance request')
    eichamt = fields.Char(string="Eichamt")
    is_downloaded = fields.Boolean(string="Downloaded", compute="_compute_downloaded_protocol")
    downloaded_user_ids = fields.Many2many('res.users', string="Downloaded users")
    begehung_id_feld = fields.Many2many('begehung', string="Begehung", store=True)
    begehungs_id = fields.Many2one('begehung', string="Test", store=True)
    begehungs_id_test = fields.Many2one('begehung_zwei', store=True)
    begehung_id_feld_zwei = fields.Many2many('begehung_zwei',  string="Begehung zwei", store=True)
    folg_erf_m = fields.Selection(related='mail_activity_id.folg_erf_m',string='Folgebegehung erforderlich?') 
    note_rel =fields.Html(related='mail_activity_id.note',string='Bemerkung')
    folg_beg_ids = fields.Many2many('folgebegehung', store=True)
    f_beg_id = fields.Many2one('folgebegehung', store=True)
    gefaehrdunsfaktor_ids = fields.Many2many('hazard.types', string='Gefahrenfaktor.', store=True)
    gefaehrdunsfaktor_betriebsanweisun_ids = fields.Many2many('hazard.types', 'protocol_equipment_type_rel', 'protocol_id', 'equipment_type_id', string='Gef.faktor')
    gefaehrdunsfaktor_id = fields.Many2one('hazard.types', string='Gefahrenfaktor', store=True)
    gef_verzeichnis_ids = fields.Many2many('gefahrstoff.verzeichnis', string="Gefahrstoff Verzeichnis", store=True)
    unterweisung_ids = fields.Many2many('unterweisung', string="Unterweisung", store=True)
    inhalte = fields.Text(string='Unterweisungsinhalte')
    name_leitung = fields.Char(string='Unterschrift der Leitung')
    signature_leiter = fields.Binary(string='Signatur Leitung')
    note_u = fields.Text(string='Anmerkung')
    protective_measures = fields.Html(string="Schutzmaßnahmen und Verhaltensregeln")
    malfunctions = fields.Html(string="Verhalten bei Störungen / Verhalten bei Gefahrfall")
    first_aid = fields.Html(string="Verhalten bei Unfällen, Erste Hilfe")
    maintenance_cleaning = fields.Html(string="Instandhaltung, Reinigung, Entsorgung")
    consequences = fields.Html(string="Folgen der Nichtbeachtung")
    hazardous_material_designation = fields.Html(string='Gefahrstoffbezeichnung')
    release_date = fields.Date(string="Freigabedatum")
    review_date = fields.Date(string="Nächster Überprüfungstermin dieser Betriebsanweisung")

    
    
    @api.depends('downloaded_user_ids')
    def _compute_downloaded_protocol(self):
        for rec in self:
            rec.is_downloaded = False
            if rec._uid in rec.downloaded_user_ids.ids:
                rec.is_downloaded = True

    @api.depends('mail_activity_id.equipment_test_type_id', 'maintenance_request_id')
    def _compute_equipment_test_type(self):
        for rec in self:
            rec.equipment_test_type = False
            if rec.mail_activity_id.equipment_test_type_id:
                rec.equipment_test_type = rec.mail_activity_id.equipment_test_type_id.equipment_test_type
            if rec.maintenance_request_id:
                rec.equipment_test_type = 'repairs'

    @api.model
    def create(self, vals):
        res = super(HazardProtocol, self).create(vals)
        if res and res.equipment_id and res.order_date:
            res.equipment_id.letzte_eichung = res.order_date
        return res

    @api.onchange("order_date")
    def _onchange_order_date(self):
        last_protocol = False
        if self.equipment_id.protocols_ids:
            last_protocol = self.equipment_id.protocols_ids.sorted(key=lambda protocol: protocol.create_date)[-1]
        if self.order_date and self.equipment_id and last_protocol and self._origin.id == last_protocol.id:
            self.equipment_id.letzte_eichung = self.order_date

    def _get_report_filename(self):
        name =  self.order_date.strftime('%y_%m_%d')
        if self.serial_no:
            name +='_'+self.serial_no
        if self.mail_activity_id.activity_type_id.name:
            name += '_'+self.mail_activity_id.activity_type_id.name
        return name

    @api.onchange("contractor_id")
    def _onchange_contractor(self):
        """Change contractor."""
        if self.contractor_id and self.contractor_id.digital_signature:
            self.signature = self.contractor_id.digital_signature
