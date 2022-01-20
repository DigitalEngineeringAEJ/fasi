# -*- coding: utf-8 -*-

import base64
from odoo import api, fields, models, _
from dateutil.relativedelta import relativedelta
from datetime import date
from datetime import datetime
from odoo.exceptions import ValidationError
from collections import defaultdict
import calendar

class EquipmentMailActivity(models.AbstractModel):
    _name = 'equipment.mail.activity'
    _description = 'Equipment Mail Activity'

    signature = fields.Binary(string='Signature')
    type = fields.Char(string='Type')
    equipment_id = fields.Many2one('maintenance.equipment', compute='_get_equipment', string='Equipment', store=True)
    date_action = fields.Datetime('Date current action', required=False, readonly=False, index=True, default=lambda self: fields.datetime.now())


class MailActivity(models.Model):
    _name = 'mail.activity'
    _inherit = ['mail.activity', 'equipment.mail.activity', 'mail.thread']
    _description = 'Mail Activity'
    
    def _get_default_malfunctions(self):
        result = """
        <table class="table table-bordered">
        <tbody>
            <tr>
                <td></td>
                <td></td>
            </tr>
        </tbody>
        </table>"""
        return result

    def _get_default_protective_measures(self):
        result = """
        <table class="table table-bordered">
        <tbody>
            <tr>
                <td></td>
                <td></td>
            </tr>
        </tbody>
        </table>"""
        return result
    def _get_default_first_aid(self):
        result = """
        <table class="table table-bordered">
        <tbody>
            <tr>
                <td></td>
                <td></td>
            </tr>
        </tbody>
        </table>"""
        return result

    def _get_default_protective_maintenance_cleaning(self):
        result = """
        <table class="table table-bordered">
        <tbody>
            <tr>
                <td></td>
                <td></td>
            </tr>
        </tbody>
        </table>"""
        return result
    
    def _get_default_consequences(self):
        result = """
        <table class="table table-bordered">
        <tbody>
            <tr>
                <td></td>
                <td></td>
            </tr>
        </tbody>
        </table>"""
        return result

    def _get_default_hazardous_material_designation(self):
        result = """
        <table class="table table-bordered">
        <tbody>
            <tr>
                <td></td>
                <td></td>
            </tr>
        </tbody>
        </table>"""
        return result

    category_id = fields.Many2one(related='equipment_id.category_id', string='Equipment Category', store=True, readonly=False)
    active = fields.Boolean(default=True)
    equipment_id = fields.Many2one('maintenance.equipment', compute='_get_equipment', string='Equipment', store=True)
    equipment_ids = fields.Many2many(comodel_name='maintenance.equipment', relation='mail_activity_maintenance_equipment_rel',
                                     column1='activity_id', column2='equipment_id', string='Equipments')
    equipment_service_id = fields.Many2one(related='equipment_id.equipment_service_id', string='Service strain"', store=True, readonly=False)
    customer_id = fields.Many2one('res.partner', compute='_get_customer', string='Customer', ondelete='set null', store=True)
    customer_ids = fields.Many2many(comodel_name='res.partner', relation='mail_activity_res_partner_rel',
                                    column1='activity_id', column2='customer_id', string='Customers')
    customer = fields.Char(related='equipment_id.customer_id.name', string='Equipment Customer', readonly=True) #Kunde
    # Kundennummer einbauen --> 26.12.2020
    ref = fields.Char(related='equipment_id.customer_id.ref', string="Kundennummer")
    customer_base = fields.Char(related='customer_id.name', readonly=True) # Kundenstamm
    equipment_test_type_id = fields.Many2one(related='activity_type_id.equipment_test_type_id', store=True, readonly=False)
    equipment_test_type = fields.Selection(related='activity_type_id.equipment_test_type_id.equipment_test_type', store=True, readonly=True)
    test_equipment_ids = fields.Many2many(related="equipment_id.equipment_service_id.test_equipment_ids", string='Test Equipments')
    equipment_protocol_id = fields.Many2one('equipment.protocol', string="Protocol", ondelete="set null")
    test_completed = fields.Boolean(string='Test Completed', default=False)
    test_fail = fields.Boolean(string='Test Fail', default=False)
    month_more = fields.Boolean(compute='_compute_activity_months', string="> 3 Months Before Final Date")
    month_less = fields.Boolean(compute='_compute_activity_months', string='< 3 Months Before Final Date')
    month_late = fields.Boolean(compute='_compute_activity_months', string='< 1 Months Late')
    planning = fields.Selection([('basic_plan', 'Basic Planning'), ('detail_plan', 'Detail Planning')], string="Planning", default="basic_plan")
    schedule_date = fields.Datetime('Scheduled Date', help="Date the detail activity plans the equipment.")
    duration = fields.Float(help="Duration in hours.")
    serial_no = fields.Char('Serial Number')
    testing_device_name = fields.Char(related='equipment_id.equipment_type_id.name', string='testing_device_name', readonly=True)
    testing_device_sn = fields.Char(related='equipment_id.equipment_type_id.types_sn', string='testing_device_sn', readonly=True)
    zip2 = fields.Char(related='customer_id.zip2', string='Zip2', store=True, readonly=True)
    customer_street = fields.Char(related='customer_id.street', string='Street', store=True, readonly=True)
    customer_zip = fields.Char(related='customer_id.zip', string='ZIP', store=True, readonly=True)
    customer_city = fields.Char(related='customer_id.city', string='City', store=True, readonly=True)
    schedule_activity_type_ids = fields.One2many('schedule.activity.type', 'mail_activity_id', string="Activity Types")
    test_specification_ids = fields.One2many('mail.activity.test', 'mail_activity_id', string="Tests Specification")
    note_tore = fields.Text(string="Note Tore")
    measuring_ids = fields.One2many('mail.activity.measuring', 'mail_activity_id', string="Measuring")
    max_difference_ids = fields.One2many('mail.activity.max.difference', 'mail_activity_id', string="Max difference")
    month = fields.Char(string="Monat: ")
    year = fields.Char(string="Jahr: ")
    is_manufacturer = fields.Boolean(string="des Herstellers oder Importeurs")
    begehung_id_feld = fields.One2many('begehung', 'name',  store=True)
    begehung_id_feld_zwei = fields.One2many('begehung_zwei', 'name_drei', store=True)
    folg_erf_m =fields.Selection([('1', 'Ja'),
                               ('0', 'Nein')],
                              string='Folgebegehung erforderlich?')
    folg_beg_ids = fields.One2many('folgebegehung', 'id_ref', string="Folgebegehung", store=True)
    gefaehrdunsfaktor_ids = fields.One2many('equipment.types', 'name', string="Gefährdungsfaktor Gruppe", store=True)
    gefaehrdunsfaktor_betriebsanweisun_ids = fields.One2many('equipment.types', 'mail_activity_id')
    mail_activity_type_ids = fields.Many2many('mail.activity.type', string="Activities", compute='_compute_activities_type', store=1)
    gef_verzeichnis_ids = fields.One2many('gefahrstoff.verzeichnis', 'sequence', string="Gefahrstoff Verzeichnis", store=True)
    unterweisung_ids = fields.One2many('unterweisung', 'sequence', string="Unterweisung", store=True)
    inhalte = fields.Text(string='Unterweisungsinhalte')
    name_leitung = fields.Char(string='Unterschrift der Leitung')
    signature_leiter = fields.Binary(string='Signatur Leitung')
    note_u = fields.Text(string='Bemerkung')
    protective_measures = fields.Html(string="Schutzmaßnahmen und Verhaltensregeln",default=_get_default_protective_measures)
    malfunctions = fields.Html(string="Verhalten bei Störungen / Verhalten bei Gefahrfall", default=_get_default_malfunctions)
    first_aid = fields.Html(string="Verhalten bei Unfällen, Erste Hilfe")
    maintenance_cleaning = fields.Html(string="Instandhaltung, Reinigung, Entsorgung")
    consequences = fields.Html(string="Folgen der Nichtbeachtung")
    release_date = fields.Date(string="Freigabedatum")
    review_date = fields.Date(string="Nächster Überprüfungstermin dieser Betriebsanweisung", default=lambda self: (datetime.today() + relativedelta(days=360)))
    hazardous_material_designation = fields.Html(string='Gefahrstoffbezeichnung')


    @api.depends('equipment_id', 'equipment_id.category_id')
    def _compute_activities_type(self):
        for rec in self:
            domain = [('id', '!=',  rec.env.ref("wepelo_equipment.mail_activity_data_betriebsanweisung").id)]
            if rec.equipment_id and rec.equipment_id.category_id and rec.equipment_id.category_id in [rec.env.ref("wepelo_equipment.equipment_hebebuhne"), rec.env.ref("wepelo_equipment.equipment_tore"), rec.env.ref("wepelo_equipment.equipment_bremsprufstand")]:
                domain = []
            rec.mail_activity_type_ids = rec.env["mail.activity.type"].search(domain).ids
            
            
#     @api.depends('equipment_id', 'equipment_id.category_id')
#     def _compute_activities_type(self):
#         for rec in self:
#             domain = [('id', '!=',  rec.env.ref("wepelo_equipment.mail_activity_data_betriebsanweisung_gefahrstoffe").id)]
#             if rec.equipment_id and rec.equipment_id.category_id and rec.equipment_id.category_id in [rec.env.ref("wepelo_equipment.equipment_arbeitsstoffe"),]:
#                 domain = []
#             rec.mail_activity_type_ids = rec.env["mail.activity.type"].search(domain).ids
            
            
#     @api.depends('equipment_id', 'equipment_id.category_id')
#     def _compute_activities_type(self):
#         for rec in self:
#             domain = [('id', '!=',  rec.env.ref("wepelo_equipment.mail_activity_data_betriebsanweisung_psa").id)]
#             if rec.equipment_id and rec.equipment_id.category_id and rec.equipment_id.category_id in [rec.env.ref("wepelo_equipment.equipment_psa")]:
#                 domain = []
#             rec.mail_activity_type_ids = rec.env["mail.activity.type"].search(domain).ids


    @api.onchange('is_manufacturer')
    def _onchange_is_manufacturer(self):
        if self.is_manufacturer:
            self.is_responsible_calibration_authority = False
            self.is_state_side = False
            self.is_technical_test = False
            self.is_officially_organizations = False
            self.is_vehicle = False

    @api.depends('res_model', 'res_id')
    def _get_equipment(self):
        for activity in self:
            activity.equipment_id = False
            if activity.res_model == 'maintenance.equipment':
                equipment = activity.res_model and self.env[activity.res_model].browse(activity.res_id)
                if equipment:
                    activity.equipment_id = equipment
                    activity.summary = equipment.name
                    activity.serial_no = equipment.serial_no

    @api.depends('res_model', 'res_id', 'activity_type_id', 'customer_id', 'summary')
    def _compute_res_name(self):
        for activity in self:
            if activity.res_model == 'maintenance.equipment':
                if activity.activity_type_id and activity.customer_id and activity.summary:
                    activity.res_name = activity.activity_type_id.name +'/'+ activity.customer_id.name +'/'+activity.summary
                elif activity.activity_type_id and not activity.customer_id and not activity.summary:
                    activity.res_name = activity.activity_type_id.name
                elif activity.activity_type_id and activity.customer_id and not activity.summary:
                    activity.res_name = activity.activity_type_id.name +'/'+ activity.customer_id.name
                elif activity.activity_type_id and not activity.customer_id and activity.summary:
                    activity.res_name = activity.activity_type_id.name +'/'+ activity.summary
                elif not activity.activity_type_id and activity.customer_id and activity.summary:
                    activity.res_name = activity.customer_id.name +'/'+ activity.summary
            else:
                super(MailActivity, self)._compute_res_name()
                
    @api.onchange('activity_type_id')
    def action_generate_history_vals(self):
        if self.equipment_test_type and self.category_id and self.equipment_test_type == 'uvv' and self.category_id == self.env.ref("wepelo_equipment.equipment_hebebuhne"):
            self.test_specification_ids = False
            test_specification_data = []
            test_specification_data.append(
                self.env["mail.activity.test"].new({"test_specification": _("Typenschild")}).id)
            test_specification_data.append(
                self.env["mail.activity.test"].new({"test_specification": _("Kurzanleitung Bedienung")}).id)
            test_specification_data.append(
                self.env["mail.activity.test"].new({"test_specification": _("Warmkennzeichnung")}).id)
            test_specification_data.append(
                self.env["mail.activity.test"].new({"test_specification": _("Ausführliche Bedienungsanleitung")}).id)
            test_specification_data.append(
                self.env["mail.activity.test"].new({"test_specification": _('Kennzeichnung ,,Heben Senken"')}).id)
            test_specification_data.append(
                self.env["mail.activity.test"].new({"test_specification": _("Allgemeinzustand der Hebebühne")}).id)
            test_specification_data.append(
                self.env["mail.activity.test"].new({"test_specification": _("Abschließbarer Hauptschalter")}).id)
            test_specification_data.append(
                self.env["mail.activity.test"].new({"test_specification": _("Zustand Tragteller")}).id)
            test_specification_data.append(
                self.env["mail.activity.test"].new({"test_specification": _("Sicherung der Bolzen")}).id)
            test_specification_data.append(
                self.env["mail.activity.test"].new({"test_specification": _("Zustand/Funktion Fußabweiser")}).id)
            test_specification_data.append(
                self.env["mail.activity.test"].new({"test_specification": _("Zustand Bolzen und Lagerstellen")}).id)
            test_specification_data.append(self.env["mail.activity.test"].new(
                {"test_specification": _("Tragkonstruktion (Verformung, Risse)")}).id)
            test_specification_data.append(
                self.env["mail.activity.test"].new({"test_specification": _("Anzugsmoment Befestigungsdübel")}).id)
            test_specification_data.append(self.env["mail.activity.test"].new(
                {"test_specification": _("Fester Sitz aller tragenden Schrauben")}).id)
            test_specification_data.append(
                self.env["mail.activity.test"].new({"test_specification": _("Zustand Polyflexriemen")}).id)
            test_specification_data.append(
                self.env["mail.activity.test"].new({"test_specification": _("Zustand Tragarme")}).id)
            test_specification_data.append(
                self.env["mail.activity.test"].new({"test_specification": _("Zustand Spindelzentrierung")}).id)
            test_specification_data.append(
                self.env["mail.activity.test"].new({"test_specification": _("Zustand der Abdeckungen")}).id)
            test_specification_data.append(
                self.env["mail.activity.test"].new({"test_specification": _("Zustand Hubspindel und Tragmutter")}).id)
            test_specification_data.append(
                self.env["mail.activity.test"].new({"test_specification": _("Standsicherheit der Hebebühne")}).id)
            test_specification_data.append(
                self.env["mail.activity.test"].new({"test_specification": _("Zustand Betonboden (Risse)")}).id)
            test_specification_data.append(
                self.env["mail.activity.test"].new({"test_specification": _("Fester Sitz aller Schrauben")}).id)
            test_specification_data.append(
                self.env["mail.activity.test"].new({"test_specification": _("Zustand Elektroleitungen")}).id)
            test_specification_data.append(self.env["mail.activity.test"].new(
                {"test_specification": _("Funktionstest Hebebühne mit Fahrzeug")}).id)
            test_specification_data.append(
                self.env["mail.activity.test"].new({"test_specification": _("Funktion Tragarmarretierung")}).id)
            test_specification_data.append(
                self.env["mail.activity.test"].new({"test_specification": _('Funktionstest „Oben- und Unten-Aus"')}).id)
            test_specification_data.append(self.env["mail.activity.test"].new(
                {"test_specification": _(" Funktion elek. Gleichaufüberwachung")}).id)
            self.test_specification_ids = [(6, 0, test_specification_data)]
        if self.equipment_test_type == 'routine_test' and self.category_id == self.env.ref(
                "wepelo_equipment.equipment_bremsprufstand"):
            self.measuring_ids = False
            self.max_difference_ids = False
            measuring_data = []
            max_difference_data = []
            measuring_data.append(
                self.env["mail.activity.measuring"].new({"name": _("Nullpunkt:")}).id)
            measuring_data.append(
                self.env["mail.activity.measuring"].new({"name": _("Anzeige bei 30% Belastung:")}).id)
            measuring_data.append(
                self.env["mail.activity.measuring"].new({"name": _("Anzeige bei max Belastung:")}).id)
            self.measuring_ids = [(6, 0, measuring_data)]
            max_difference_data.append(
                self.env["mail.activity.max.difference"].new({"name": _("Anzeige bei 30% Belastung:")}).id)
            max_difference_data.append(
                self.env["mail.activity.max.difference"].new({"name": _("Anzeige bei max Belastung:")}).id)
            self.max_difference_ids = [(6, 0, max_difference_data)]
        history_vals3 = {
        'name': self.equipment_id.id,
        'current_date': self.date_action.now(),
        'topic': self.activity_type_id.name
        }
        history3 = self.env['equipment.history'].create(history_vals3)

    @api.depends('equipment_id')
    def _get_customer(self):
        for activity in self:
            activity.customer_id = activity.equipment_id.customer_id

    @api.depends('date_deadline')
    def _compute_activity_months(self):
        for activity in self:
            months = activity.date_deadline.month - date.today().month
            days = abs((activity.date_deadline - date.today()).days)
            if activity.date_deadline.month == date.today().month:
                number_days_month = calendar.monthrange(date.today().year,date.today().month)[1]
            else:
                if activity.date_deadline.day > calendar.monthrange(date.today().year,date.today().month)[1]:
                    second_date = date(date.today().year, date.today().month, calendar.monthrange(date.today().year,date.today().month)[1])
                else:
                    second_date = date(date.today().year, date.today().month, activity.date_deadline.day)
                number_days_month = (activity.date_deadline - second_date).days
            activity.month_more = False
            activity.month_late = False
            activity.month_less = False
            if not activity.test_completed:
                if ((months == 1 and days > number_days_month) or months >1) and (months < 3 or (months == 3 and days <= number_days_month)) and activity.date_deadline > date.today():
                    activity.update({'month_less': True, 'month_more': False, 'month_late': False})
                elif ((months < 1 or months == 1) and days <= number_days_month and days <= 31) or activity.date_deadline <= date.today():
                    activity.update({'month_late': True, 'month_more': False, 'month_less': False})
                else:
                    activity.update({'month_late': False, 'month_more': True, 'month_less': False})

    @api.onchange('schedule_date')
    def onchange_schedule_date(self):
        if self.schedule_date:
            self.date_deadline = self.schedule_date.date()

    def unlink(self):
        maintenance = self.filtered(lambda rec: rec.res_model == 'maintenance.equipment' and rec.active)
        records = self
        if maintenance:
            maintenance.write({'active': False})
            records = self - maintenance
        return super(MailActivity, records).unlink()

    def action_activity_fail(self):
        self.update({'test_fail': True, 'month_late': False, 'month_more': False, 'month_less': False})
        self.action_done()

    def action_generate_protocol(self):
        protocol_vals = {
            'name': self.equipment_id.name,
            'date': self.date_deadline,
            'order_date': fields.Date.context_today(self),
            'customer_id': self.customer_id.id,
            'contractor_id': self.user_id.id,
            'manufacturer_id': self.equipment_id.manufacturer_id.id,
            'mail_activity_id': self.id,
            'equipment_test_type_id': self.activity_type_id.equipment_test_type_id.id,
            'equipment_test_type': self.equipment_test_type,
            'serial_no': self.equipment_id.serial_no,
            'equipment_service_id': self.equipment_id.equipment_service_id.id,
            'signature': self.signature or False,
            #Neue Felder per 26.12.2020 
            'equipment_id':self.equipment_id.id,
            'ref':self.ref,
            'begehung_id_feld':self.begehung_id_feld,
            'begehung_id_feld_zwei':self.begehung_id_feld_zwei,
            'folg_erf_m':self.folg_erf_m or False,
            'folg_beg_ids':self.folg_beg_ids,
            'gefaehrdunsfaktor_ids':self.gefaehrdunsfaktor_ids,
            'gefaehrdunsfaktor_betriebsanweisun_ids':self.gefaehrdunsfaktor_betriebsanweisun_ids,
            'protective_measures':self.protective_measures,
            'malfunctions':self.malfunctions,
            'first_aid':self.first_aid,
            'maintenance_cleaning':self.maintenance_cleaning,
            'consequences':self.consequences,
            'gef_verzeichnis_ids':self.gef_verzeichnis_ids,
            'unterweisung_ids':self.unterweisung_ids,
            'inhalte':self.inhalte,
            'name_leitung':self.name_leitung,
            'signature_leiter':self.signature_leiter,
            'note_u':self.note_u,
            'hazardous_material_designation':self.hazardous_material_designation

        }
#         if self.equipment_test_type == 'el_test': hazardous_material_designation
#             el_test_vals = {
#                 'testing_device': self.testing_device_name,
#                 'testing_device_sn': self.testing_device_sn,
#                 'type': 'Infralyt Smart',
#             }
#             protocol_vals.update(el_test_vals)
#         if self.equipment_test_type == 'el_test':
#             el_test_vals = {
#                 'testing_device': self.testing_device_name,
#                 'testing_device_sn': self.testing_device_sn,
#                 'type': 'Opacylit 1030',
#                 'voltage_u_in_volts_v': self.voltage_u_in_volts_v,
#                 'frequency_f_in_heart_hz': self.frequency_f_in_heart_hz,
#                 'protection_class': self.protection_class,
#                 'tested_din_vde_0701_0702': self.tested_din_vde_0701_0702,
#                 'rpe': self.rpe,
#                 'operator_rpe': self.operator_rpe,
#                 'riso_m': self.riso_m,
#                 'operator_riso': self.operator_riso,
#                 'iea_ma': self.iea_ma,
#                 'operator_iea': self.operator_iea,
#                 'evaluation': self.evaluation,
#             }
#             protocol_vals.update(el_test_vals)
#         if self.equipment_test_type == 'maintenance':
#             maintenance_diesel_vals = {
#                 'exhaust_hose_probe': self.exhaust_hose_probe,
#                 'measuring_optics': self.measuring_optics,
#                 'measuring_cell': self.measuring_cell,
#                 'cables_hose_connections': self.cables_hose_connections,
#                 'manual_calibration': self.manual_calibration,
#                 'functional_control': self.functional_control,
#                 'test_filter': self.test_filter,
#                 'test_calibration_filter': self.test_calibration_filter,
#             }
#             protocol_vals.update(maintenance_diesel_vals)

#         if self.equipment_test_type == 'maintenance' and self.exhaust_measuring_device == 'petrol':
#             maintenance_petrol_vals = {
#                 'exhaust_hose_probe': self.exhaust_hose_probe,
#                 'pre_filter': self.pre_filter,
#                 'coarse_filter': self.coarse_filter,
#                 'fine_filter': self.fine_filter,
#                 'leak_test_seal': self.leak_test_seal,
#                 'leak_test_performed': self.leak_test_performed,
#                 'test_o2_sensor': self.test_o2_sensor,
#                 'test_gas': self.test_gas,
#                 'sensor_type': self.sensor_type,
#                 'sensor_serial': self.sensor_serial,
#                 'gas_certificate_no': self.gas_certificate_no,
#                 'gas_bottle_no': self.gas_bottle_no,
#                 'test_gas_concentration_co': self.test_gas_concentration_co,
#                 'test_gas_concentration_co2': self.test_gas_concentration_co2,
#                 'test_gas_concentration_c3': self.test_gas_concentration_c3,
#                 'value_after_adjustment_co': self.value_after_adjustment_co,
#                 'value_after_adjustment_co2': self.value_after_adjustment_co2,
#                 'value_after_adjustment_c3': self.value_after_adjustment_c3
#             }
#             protocol_vals.update(maintenance_petrol_vals)

        protocol = self.env['equipment.protocol'].create(protocol_vals)
        self.write({'equipment_protocol_id': protocol.id,
                    'test_completed': True,
                    'month_late': False,
                    'month_more': False,
                    'month_less': False,
                })

#         if self.equipment_test_type == 'el_test' or (self.equipment_test_type == 'maintenance' and self.exhaust_measuring_device in ['diesel', 'petrol']):
#             if self.equipment_test_type == 'el_test':
#                 report = self.env.ref('wepelo_equipment.wepelo_equipment_protocol').render_qweb_pdf(protocol.ids[0])
#             if self.equipment_test_type == 'maintenance' and self.exhaust_measuring_device in ['diesel', 'petrol']:
#                 report = self.env.ref('wepelo_equipment.wepelo_equipment_protocol_maintenance').render_qweb_pdf(protocol.ids[0])
#             filename = protocol.order_date.strftime('%y_%m_%d')+'_'+self.equipment_id.serial_no+'_'+self.activity_type_id.name+'.pdf'
#             attachment = self.env['ir.attachment'].create({
#                 'name': filename,
#                 'type': 'binary',
#                 'datas': base64.b64encode(report[0]),
#                 'store_fname': filename,
#                 'res_model': 'maintenance.equipment',
#                 'res_id': self.equipment_id.id,
#                 'mimetype': 'application/x-pdf'
#             })
#             self.equipment_id.message_post(body=_('%s Completed (originally assigned to %s)') % (self.activity_type_id.name, self.user_id.name,), attachment_ids=[attachment.id])
#         else:
#             self.equipment_id.message_post(body=_('%s Completed (originally assigned to %s)') % (self.activity_type_id.name, self.user_id.name,))

        if self.equipment_test_type != 'repairs':
            next_activity = self.copy()
            activity_after_days = self.equipment_test_type_id.cycle_duration
            next_activity.write({'date_deadline': (next_activity.date_deadline + relativedelta(days=activity_after_days)), 'equipment_protocol_id': False, 'test_completed': False, 'schedule_date': False, 'duration': 0, 'planning': 'basic_plan'})
        if protocol:
            return {
                "type": "ir.actions.act_window",
                "res_model": "equipment.protocol",
                "view_mode": "form",
                "res_id": protocol.id,
        }

    @api.onchange('planning')
    def onchange_planning(self):
        if self.planning:
            self.schedule_date = False
            self.duration = 0

    def activity_edit(self):
        return {
            "name": _("Detail Planning"),
            "res_model": "mail.activity.edit.wizard",
            "view_mode": "form",
            "type": "ir.actions.act_window",
            "target": "new",
            'context': {
                'activity_ids': self.ids,
            }
        }

    @api.onchange("user_id")
    def _onchange_user(self):
        """Change user."""
        if self.user_id and self.user_id.digital_signature:
            self.signature = self.user_id.digital_signature

    @api.model
    def create(self, vals):
        res = super(MailActivity, self).create(vals)
        if res:
            res.signature = res.user_id.digital_signature
            if res.equipment_test_type == 'uvv' and res.category_id == self.env.ref("wepelo_equipment.equipment_hebebuhne"):
                test_specification_data = []
                test_specification_data.append(self.env["mail.activity.test"].create({"test_specification": _("Typenschild")}).id)
                test_specification_data.append(self.env["mail.activity.test"].create({"test_specification": _("Kurzanleitung Bedienung")}).id)
                test_specification_data.append(self.env["mail.activity.test"].create({"test_specification": _("Warmkennzeichnung")}).id)
                test_specification_data.append(self.env["mail.activity.test"].create({"test_specification": _("Ausführliche Bedienungsanleitung")}).id)
                test_specification_data.append(self.env["mail.activity.test"].create({"test_specification": _('Kennzeichnung ,,Heben Senken"')}).id)
                test_specification_data.append(self.env["mail.activity.test"].create({"test_specification": _("Allgemeinzustand der Hebebühne")}).id)
                test_specification_data.append(self.env["mail.activity.test"].create({"test_specification": _("Abschließbarer Hauptschalter")}).id)
                test_specification_data.append(self.env["mail.activity.test"].create({"test_specification": _("Zustand Tragteller")}).id)
                test_specification_data.append(self.env["mail.activity.test"].create({"test_specification": _("Sicherung der Bolzen")}).id)
                test_specification_data.append(self.env["mail.activity.test"].create({"test_specification": _("Zustand/Funktion Fußabweiser")}).id)
                test_specification_data.append(self.env["mail.activity.test"].create({"test_specification": _("Zustand Bolzen und Lagerstellen")}).id)
                test_specification_data.append(self.env["mail.activity.test"].create({"test_specification": _("Tragkonstruktion (Verformung, Risse)")}).id)
                test_specification_data.append(self.env["mail.activity.test"].create({"test_specification": _("Anzugsmoment Befestigungsdübel")}).id)
                test_specification_data.append(self.env["mail.activity.test"].create({"test_specification": _("Fester Sitz aller tragenden Schrauben")}).id)
                test_specification_data.append(self.env["mail.activity.test"].create({"test_specification": _("Zustand Polyflexriemen")}).id)
                test_specification_data.append(self.env["mail.activity.test"].create({"test_specification": _("Zustand Tragarme")}).id)
                test_specification_data.append(self.env["mail.activity.test"].create({"test_specification": _("Zustand Spindelzentrierung")}).id)
                test_specification_data.append(self.env["mail.activity.test"].create({"test_specification": _("Zustand der Abdeckungen")}).id)
                test_specification_data.append(self.env["mail.activity.test"].create({"test_specification": _("Zustand Hubspindel und Tragmutter")}).id)
                test_specification_data.append(self.env["mail.activity.test"].create({"test_specification": _("Standsicherheit der Hebebühne")}).id)
                test_specification_data.append(self.env["mail.activity.test"].create({"test_specification": _("Zustand Betonboden (Risse)")}).id)
                test_specification_data.append(self.env["mail.activity.test"].create({"test_specification": _("Fester Sitz aller Schrauben")}).id)
                test_specification_data.append(self.env["mail.activity.test"].create({"test_specification": _("Zustand Elektroleitungen")}).id)
                test_specification_data.append(self.env["mail.activity.test"].create({"test_specification": _("Funktionstest Hebebühne mit Fahrzeug")}).id)
                test_specification_data.append(self.env["mail.activity.test"].create({"test_specification": _("Funktion Tragarmarretierung")}).id)
                test_specification_data.append(self.env["mail.activity.test"].create({"test_specification": _('Funktionstest „Oben- und Unten-Aus"')}).id)
                test_specification_data.append(self.env["mail.activity.test"].create({"test_specification": _("Funktion elek. Gleichaufüberwachung")}).id)
                res.test_specification_ids = [(6, 0, test_specification_data)]
            if res.equipment_test_type == 'routine_test' and res.category_id == self.env.ref("wepelo_equipment.equipment_bremsprufstand"):
                measuring_data = []
                max_difference_data = []
                measuring_data.append(
                    self.env["mail.activity.measuring"].create({"name": _("Nullpunkt:")}).id)
                measuring_data.append(
                    self.env["mail.activity.measuring"].create({"name": _("Anzeige bei 30% Belastung:")}).id)
                measuring_data.append(
                    self.env["mail.activity.measuring"].create({"name": _("Anzeige bei max Belastung:")}).id)
                res.measuring_ids = [(6, 0, measuring_data)]
                max_difference_data.append(
                    self.env["mail.activity.max.difference"].create({"name": _("Anzeige bei 30% Belastung:")}).id)
                max_difference_data.append(
                    self.env["mail.activity.max.difference"].create({"name": _("Anzeige bei max Belastung:")}).id)
                res.max_difference_ids = [(6, 0, max_difference_data)]
            gefaehrdunsfaktor_betriebsanweisun_data = []
            if res.equipment_test_type == 'betriebsanweisung':
                last_activity_gefahrenquelle = self.search(
                    [("equipment_id", '=', res.equipment_id.id), ('activity_type_id', '=', self.env.ref("wepelo_equipment.mail_activity_data_calibration_ei").id)],
                    order='id desc', limit=1)
                if last_activity_gefahrenquelle:
                    for gefaehrdunsfaktor in last_activity_gefahrenquelle.gefaehrdunsfaktor_ids:
                        gefaehrdunsfaktor_betriebsanweisun = self.env['equipment.types'].create({
                            'gefaehrdungsf_name': gefaehrdunsfaktor.gefaehrdungsf_name.id,
                            'gefahrenquellen_typ_id': gefaehrdunsfaktor.gefahrenquellen_typ_id.id,
                            'gefahrenquellen_typ_beschreibung': gefaehrdunsfaktor.gefahrenquellen_typ_beschreibung,
                            'gef_beurteilung_w': gefaehrdunsfaktor.gef_beurteilung_w,
                            'gef_beurteilung_a': gefaehrdunsfaktor.gef_beurteilung_a,
                            'gef_beurteilung_e': gefaehrdunsfaktor.gef_beurteilung_e,
                            'klasse_gef': gefaehrdunsfaktor.klasse_gef,
                            'abstellmassnahme_gef_kla': gefaehrdunsfaktor.abstellmassnahme_gef_kla,
                            'abs_gef': gefaehrdunsfaktor.abs_gef,
                            'deadline_abs_gef': gefaehrdunsfaktor.deadline_abs_gef,
                            'verantwortlich_gef': gefaehrdunsfaktor.verantwortlich_gef,
                            'folg_beg_gef': gefaehrdunsfaktor.folg_beg_gef,
                        })
                        gefaehrdunsfaktor_betriebsanweisun_data.append(gefaehrdunsfaktor_betriebsanweisun.id)
                res.gefaehrdunsfaktor_betriebsanweisun_ids = [(6, 0, gefaehrdunsfaktor_betriebsanweisun_data)]

        return res

    def action_close_dialog(self):
        if not self.activity_type_id and self.schedule_activity_type_ids:
            # create activity for all schedule activity type
            for schedule_activity_type in self.schedule_activity_type_ids:
                self.env['mail.activity'].create({
            'activity_type_id': schedule_activity_type.activity_type_id.id,
            'summary': self.summary or schedule_activity_type.activity_type_id.summary,
            'automated': True,
            'note': self.note or schedule_activity_type.activity_type_id.default_description,
            'date_deadline': schedule_activity_type.date_deadline,
            'res_model_id': self.res_model_id.id,
            'res_model': self.res_model,
            'user_id': self.user_id.id or schedule_activity_type.activity_type_id.default_user_id.id or self.env.uid,
             'res_id': self.res_id
        })
        not_activity_types = self.env['mail.activity'].search([("activity_type_id", "=", False),("res_model_id", "=", self.res_model_id.id),("res_model", "=", self.res_model), ("res_id", "=", self.res_id)])
        for not_activity_type in not_activity_types:
            if not_activity_type.res_model == 'maintenance.equipment':
                not_activity_type.sudo().unlink()
            not_activity_type.sudo().unlink()
        return {'type': 'ir.actions.act_window_close'}

    @api.constrains("schedule_activity_type_ids", "activity_type_id")
    def _check_schedule_activity_type(self):
        for record in self:
            if not record.schedule_activity_type_ids and not record.activity_type_id:
                raise ValidationError(_("You should add Activity Type"))

    def _action_done(self, feedback=False, attachment_ids=None):
        messages = self.env['mail.message']
        next_activities_values = []

        # Search for all attachments linked to the activities we are about to unlink. This way, we
        # can link them to the message posted and prevent their deletion.
        attachments = self.env['ir.attachment'].search_read([
            ('res_model', '=', self._name),
            ('res_id', 'in', self.ids),
        ], ['id', 'res_id'])

        activity_attachments = defaultdict(list)
        for attachment in attachments:
            activity_id = attachment['res_id']
            activity_attachments[activity_id].append(attachment['id'])
        for activity in self:
            # post message on activity, before deleting it
            # if the activity contain many activity types
            if activity.schedule_activity_type_ids and not activity.activity_type_id:
                for schedule_activity_type in activity.schedule_activity_type_ids:
                    # create activity for all schedule activity type
                    activity_done = self.create({
                        'activity_type_id': schedule_activity_type.activity_type_id.id,
                        'summary': activity.summary or schedule_activity_type.activity_type_id.summary,
                        'automated': True,
                        'note': activity.note or schedule_activity_type.activity_type_id.default_description,
                        'date_deadline': schedule_activity_type.date_deadline,
                        'res_model_id': activity.res_model_id.id,
                        'res_model': activity.res_model,
                        'user_id': activity.user_id.id or schedule_activity_type.activity_type_id.default_user_id.id or activity.env.uid,
                        'res_id': activity.res_id
                    })
                    # schedule the next activity type
                    if activity_done.activity_type_id:
                        if activity_done.force_next:
                            Activity = self.env['mail.activity'].with_context(
                                activity_previous_deadline=activity_done.date_deadline)  # context key is required in the onchange to set deadline
                            vals = Activity.default_get(Activity.fields_get())

                            vals.update({
                                'previous_activity_type_id': activity_done.activity_type_id.id,
                                'res_id': activity_done.res_id,
                                'res_model': activity_done.res_model,
                                'res_model_id': self.env['ir.model']._get(activity_done.res_model).id,
                            })
                            virtual_activity = Activity.new(vals)
                            virtual_activity._onchange_previous_activity_type_id()
                            virtual_activity._onchange_activity_type_id()
                            next_activities_values.append(virtual_activity._convert_to_write(virtual_activity._cache))
                            if self.res_model == 'maintenance.equipment':
                                self.unlink()
                        record = self.env[activity_done.res_model].browse(activity_done.res_id)
                        # archive all schedule activity type
                        record.message_post_with_view(
                            'mail.message_activity_done',
                            values={
                                'activity': activity_done,
                                'feedback': feedback,
                                'display_assignee': activity.user_id != self.env.user
                            },
                            subtype_id=self.env['ir.model.data'].xmlid_to_res_id('mail.mt_activities'),
                            mail_activity_type_id=activity_done.activity_type_id.id,
                            attachment_ids=[(4, attachment_id) for attachment_id in attachment_ids] if attachment_ids else [],
                        )
                        activity_message = record.message_ids[0]
                        message_attachments = self.env['ir.attachment'].browse(activity_attachments[activity_done.id])
                        if message_attachments:
                            message_attachments.write({
                                'res_id': activity_message.id,
                                'res_model': activity_message._name,
                            })
                            activity_message.attachment_ids = message_attachments
                        messages |= activity_message
                        activity_done.unlink()
                    not_activity_types = activity.search(
                        [("activity_type_id", "=", False), ("res_model_id", "=", activity.res_model_id.id),
                         ("res_model", "=", activity.res_model), ("res_id", "=", activity.res_id)])
                    for not_activity_type in not_activity_types:
                        if not_activity_type.res_model == 'maintenance.equipment':
                            not_activity_type.sudo().unlink()
            else:
                # if the activity contain one activity type
                if activity.force_next:
                    Activity = self.env['mail.activity'].with_context(
                        activity_previous_deadline=activity.date_deadline)  # context key is required in the onchange to set deadline
                    vals = Activity.default_get(Activity.fields_get())

                    vals.update({
                        'previous_activity_type_id': activity.activity_type_id.id,
                        'res_id': activity.res_id,
                        'res_model': activity.res_model,
                        'res_model_id': self.env['ir.model']._get(activity.res_model).id,
                    })
                    virtual_activity = Activity.new(vals)
                    virtual_activity._onchange_previous_activity_type_id()
                    virtual_activity._onchange_activity_type_id()
                    next_activities_values.append(virtual_activity._convert_to_write(virtual_activity._cache))
                record = self.env[activity.res_model].browse(activity.res_id)
                record.message_post_with_view(
                    'mail.message_activity_done',
                    values={
                        'activity': activity,
                        'feedback': feedback,
                        'display_assignee': activity.user_id != self.env.user
                    },
                    subtype_id=self.env['ir.model.data'].xmlid_to_res_id('mail.mt_activities'),
                    mail_activity_type_id=activity.activity_type_id.id,
                    attachment_ids=[(4, attachment_id) for attachment_id in attachment_ids] if attachment_ids else [],
                )

                # Moving the attachments in the message
                # directly, see route /web_editor/attachment/add
                activity_message = record.message_ids[0]
                message_attachments = self.env['ir.attachment'].browse(activity_attachments[activity.id])
                if message_attachments:
                    message_attachments.write({
                        'res_id': activity_message.id,
                        'res_model': activity_message._name,
                    })
                    activity_message.attachment_ids = message_attachments
                messages |= activity_message
                begehung_id_feld_zwei = activity.mapped('begehung_id_feld_zwei').filtered(
                lambda x: x.folg_erf_m == 'Ja')
            if len(begehung_id_feld_zwei)> 0:
                #activity_after_days = activity.equipment_test_type_id.cycle_duration
                schedule_activity_type = self.env['mail.activity.type'].search(
                    [('id', '=',  self.env.ref('wepelo_equipment.mail_activity_data_el_test').id)])
                new_act = self.create({
                    'planning': 'basic_plan', 'equipment_test_type': 'el_test',
                    'activity_type_id': schedule_activity_type.id,
                    'summary': activity.summary or False,
                    'automated': True,
                    'note': activity.note or '',
                    'date_deadline': activity.date_deadline,
                    'res_model_id': activity.res_model_id.id,
                    'res_model': activity.res_model,
                    'user_id': activity.user_id.id or activity.env.uid,
                    'res_id': activity.res_id,
                })
                vals = []
                for begehung_id in activity.begehung_id_feld_zwei:
                    if begehung_id.folg_erf_m == 'Ja':
                        val = {
                            'nummer_vier': begehung_id.nummer_drei,
                            'name_vier': begehung_id.name_zwei,
                            'klasse_drei': begehung_id.klasse_zwei,
                            'abstellmassnahme_drei': begehung_id.abstellmassnahme_zwei,
                            'abstellmassnahme_k_drei': begehung_id.abstellmassnahme_k_zwei,
                            'deadline_abs_ref': begehung_id.deadline_abs,
                            'verantwortlich_ref' : begehung_id.verantwortlich.id,
                            'id_ref': new_act.id,
                        }
                        vals.append((0, 0, val))
                new_act.write({'folg_beg_ids': vals})
        next_activities = self.env['mail.activity'].create(next_activities_values)
        self.unlink()  # will unlink activity, dont access `self` after that
        sequence = self.env['ir.sequence'].search([('code', '=', 'begehung.eins')])
        sequence.number_next_actual = 1
        sequence_zwei = self.env['ir.sequence'].search([('code', '=', 'begehung.zwei')])
        sequence_zwei.number_next_actual = 1
        return messages, next_activities


class MailActivityType(models.Model):
    _inherit = 'mail.activity.type'

    new_signature = fields.Binary(string='New Signature')
    equipment_test_type_id = fields.Many2one('equipment.test', string="Equipment Test")

    @api.onchange('equipment_test_type_id')
    def onchange_equipment_test_type(self):
        if self.equipment_test_type_id:
            self.name = self.equipment_test_type_id.display_name
            

class ScheduleActivityType(models.Model):
    _name = 'schedule.activity.type'
    _description = 'Schedule Activity Type'
    _order = 'activity_type_id'

    res_model_id = fields.Many2one(
        'ir.model', string='Document Model',
        index=True, related='mail_activity_id.res_model_id', compute_sudo=True, store=True, readonly=True)
    date_deadline = fields.Date('Due Date', index=True, required=True, default=fields.Date.context_today)
    activity_type_id = fields.Many2one('mail.activity.type', string='Activity Type', required=1)
    mail_activity_id = fields.Many2one('mail.activity', string="Mail Activity")
    equipment_service_id = fields.Many2one(related='mail_activity_id.equipment_id.equipment_service_id', string='Service strain')
    mail_activity_type_ids = fields.Many2many('mail.activity.type', string="Mail Activity Types", compute="_compute_mail_activity_types")

    @api.depends("mail_activity_id.test_equipment_ids", "res_model_id")
    def _compute_mail_activity_types(self):
        for rec in self:
            domain = ['|', ('res_model_id', '=', False), ('res_model_id', '=', rec.res_model_id.id)]
            if rec.mail_activity_id.equipment_service_id:
                domain = [
                    ("equipment_test_type_id", "in", rec.mail_activity_id.test_equipment_ids.ids),

                ]
            activity_types = rec.env["mail.activity.type"].search(domain)
            rec.mail_activity_type_ids = activity_types.ids


class MailActivityTest(models.Model):
    _name = 'mail.activity.test'
    _description = 'Mail Activity Test'

    mail_activity_id = fields.Many2one('mail.activity', string='Mail Activity')
    test_specification = fields.Char(string="Prüfschrift")
    is_success = fields.Boolean(string="In Ordnung")
    is_failed = fields.Boolean(string="Mängel fehlt")
    is_after_examination = fields.Boolean(string="Nachprüfung")
    note = fields.Text(string="Bemerkung")


class MailActivityMeasuring(models.Model):
    _name = 'mail.activity.measuring'
    _description = 'Mail Activity Measuring'

    name = fields.Char(string="Messbereich: vorne/hinten oder")
    left_large = fields.Float(string="links groß")
    right_large = fields.Float(string="rechts groß")
    max_error_large = fields.Float(string="max.Fehler groß")
    left_small = fields.Float(string="links klein")
    right_small = fields.Float(string="rechts klein")
    max_error_small = fields.Float(string="max.Fehler klein")
    mail_activity_id = fields.Many2one('mail.activity', string='Mail Activity')


class MailActivityMaxDifference(models.Model):
    _name = 'mail.activity.max.difference'
    _description = 'Mail Activity Max Difference'

    name = fields.Char(string="Max Differenz der Anzeige links/rechts")
    kn = fields.Float(string="[kN]")
    percentage = fields.Float(string="[%]")
    mail_activity_id = fields.Many2one('mail.activity', string='Mail Activity')
