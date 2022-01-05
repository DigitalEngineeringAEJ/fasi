# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class TestEquipmentService(models.Model):
    _name = 'equipment.service'
    _description = 'Service strain'

    name = fields.Char(string='Name')
    test_equipment_ids = fields.Many2many('equipment.test', 'equipment_service_equipment_test_rel', 'equipment_service_id', 'equipment_test_id', string='Test Equipment')
    is_maintenance = fields.Boolean(string="Maintenance", compute='_is_maintenance', store=True)

    @api.depends('test_equipment_ids')
    def _is_maintenance(self):
        for service in self:
            if any(test_equipment.equipment_test_type == 'maintenance' for test_equipment in service.test_equipment_ids):
                service.is_maintenance = True
            else:
                service.is_maintenance = False


class EquipmentTest(models.Model):
    _name = 'equipment.test'
    _description = 'Test Equipment'
    _rec_name = 'display_name'

    display_name = fields.Char(compute='_get_display_name', string='Name', readonly=False, store=True)
    equipment_test_type = fields.Selection(selection='_get_equipment_test_type', string='Test strain')
    cycle_duration = fields.Integer(string='Cycle Duration', default=0)

    def _get_equipment_test_type(self):
        return [
            ('calibration_ei', _('Gefährdungsbeurteilung')),
            ('el_test', _('Folgebegehung')),
            ('routine_test', _('Begehung')),
            ('calibration', _('Kalibrierung')),
            ('betriebsanweisung', _('Betriebsanweisung')),
            ('uvv', _('Betriebssicherheitsprüfung')),
            ('maintenance', _('Wartung')),
            ('repairs', _('Reparaturen')),
            ('gefahrstoff_verszeichnis', _('Gefahrstoff-Verszeichnis')),
            ('unterweisung', _('Unterweisung')),
            ('betriebsanweisung_gefahrstoffe', _('Betriebsanweisung Gefahrstoffe')),
        ]

    equipment_test_types = {
        'calibration_ei': _('Gefährdungsbeurteilung'),
        'el_test': _('Folgebegehung'),
        'routine_test': _('Begehung'),
        'calibration': _('Kalibrierung'),
        'betriebsanweisung': _('Betriebsanweisung'),
        'uvv': _('Betriebssicherheitsprüfung'),
        'maintenance': _('Wartung'),
        'repairs': _('Reparaturen'),
        'gefahrstoff_verszeichnis': _('Gefahrstoff-Verszeichnis'),
        'unterweisung': _('Unterweisung'),
    }
# 
#     @api.depends('equipment_test_type', 'cycle_duration')
#     def _get_display_name(self):
#         if self.equipment_test_type:
#             self.display_name = self.equipment_test_types.get(self.equipment_test_type) + ' (' + str(self.cycle_duration) + ')'


class TestEquipment(models.Model):
    _name = 'test.equipment.device'
    _description = 'Test Equipment'
    
    name = fields.Char(string='Name')
    sn = fields.Char(string='S/N')
    x_zertnum = fields.Char(string='Zertifikatsnummer') 
    x_flaschnum = fields.Char(string='Flaschennummer')
    x_gasco = fields.Float(string='Prüfgas Konzentration (CO)')
    x_gasco2 = fields.Float(string='Prüfgas Konzentration (CO2)')
    x_gasc3 = fields.Float(string='Prüfgas Konzentration (C3)')
    x_device_typ = fields.Selection([('testgas', 'Test gas'), ('platzhalter', 'Platzhalter')], string='Device Typ')