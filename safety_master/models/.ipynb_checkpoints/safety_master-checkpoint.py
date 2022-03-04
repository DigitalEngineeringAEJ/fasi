# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo import exceptions
from re import search
from dateutil.relativedelta import relativedelta
from datetime import date, datetime, timedelta
import re
import ast

class SafetyMaster(models.Model):
    _name = 'safety.master'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Safety Master'
    _check_company_auto = True

    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, record.name))
        return result

    category_id = fields.Many2one('hazard.category', string='Equipment Category',
                                  tracking=True)
    user_id = fields.Many2one('res.users', string='Technician', tracking=True)
    name = fields.Char('Equipment Name', required=True, translate=True)

    owner_user_id = fields.Many2one('res.users', string='Owner', tracking=True)
    assign_date = fields.Date('Assigned Date', tracking=True)
    serial_no = fields.Char('Serial Number', copy=False)
    technician_user_id = fields.Many2one('res.users', string='Technician', tracking=True)
    maintenance_ids = fields.One2many('hazard.request', 'equipment_id')
    maintenance_open_count = fields.Integer(compute='_compute_maintenance_count', string="Current Maintenance",
                                            store=True)

    active = fields.Boolean(default=True)
    next_action_date = fields.Date(compute='_compute_next_maintenance',
                                   string='Date of the next preventive maintenance', store=True)
    model = fields.Char('Model')
    category_id = fields.Many2one('hazard.category', string='Equipment Category',
                                  tracking=True)
    partner_id = fields.Many2one('res.partner', string='Vendor', check_company=True)
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company)
    color = fields.Integer('Color Index')
    partner_ref = fields.Char('Vendor Reference')
    effective_date = fields.Date('Effective Date', default=fields.Date.context_today, required=True,
                                 help="Date at which the equipment became effective. This date will be used to compute the Mean Time Between Failure.")
    warranty_date = fields.Date('Warranty Expiration Date')
    note = fields.Text('Comments', translate=True)
    maintenance_team_id = fields.Many2one('hazard.team', string='Maintenance Team', check_company=True)
    location = fields.Char('Location')
    period = fields.Integer('Days between each preventive maintenance')
    maintenance_duration = fields.Float(help="Maintenance Duration in hours.")
    equipment_count = fields.Integer(string="Equipment", compute='_compute_equipment_count')
    maintenance_count = fields.Integer(string="maintenance Count", compute='_compute_maintenance_count')
    alias_id = fields.Many2one(
        'mail.alias', 'Alias', ondelete='restrict', required=True,
        help="Email alias for this equipment category. New emails will automatically "
             "create a new equipment under this category.")
   # contact_person = fields.Char(related='customer_id.contact_person', string='Contact Person', readonly=True, store=True)
    activity_id = fields.Many2one('mail.activity', string='Activity', store=True, ondelete='set null')
    activity_ids = fields.One2many('mail.activity', 'equipment_id')
    pipeline_status = fields.Selection([('status1', 'Start Production'), ('status2', 'Data')], string='Pipeline Status Bar')
    house_no = fields.Char( compute='_compute_house_no', string='House Number')
    manufacturer_id = fields.Many2one('res.partner', string='Manufacturer', ondelete='set null', domain="[('type', '=', 'manufacturer')]")
    inventory_number = fields.Char(string='Inventory Number')
    customer_id = fields.Many2one('res.partner', string='Customer', ondelete='set null', domain="[('type', 'not in', ('manufacturer', 'vendor')), ('is_company', '=', True), ('parent_id', '=', False)]")
    partner_id = fields.Many2one('res.partner', string='Vendor', ondelete='set null', domain="[('type', '=', 'vendor')]")
    email = fields.Char(related='customer_id.email', string='Email', readonly=True, store=True)
    mobile = fields.Char(related='customer_id.mobile', string='Mobile', readonly=True, store=True)
    zip = fields.Char(related='customer_id.zip', string='Zip', readonly=True, store=True)
    test_equipment_device_id = fields.Many2one('hazard.equipment.device', string='Testing Device', ondelete='set null')
    equipment_service_id = fields.Many2one('hazard.service', string='Service strain', ondelete='set null')
    city = fields.Char(related='customer_id.city', string='City', readonly=True, store=True)
    street = fields.Char(string='Street', compute="_compute_house_no")
    phone = fields.Char(related='customer_id.phone', string='Phone Number', readonly=True, store=True)
    test_device_name = fields.Many2one('hazard.equipment.device', string='Test Gas', store=True, ondelete='set null')
    protocol_number = fields.Integer(string="Protocol Number", compute='_compute_protocol_number')
    planing_count = fields.Integer(string="Planing", compute='_compute_planing_count')
    protocols_ids = fields.One2many('hazard.protocol', 'equipment_id')
    protocol_count = fields.Integer(string="Protocol", compute='_compute_protocol_count')
    equipment_type_id = fields.Many2one('hazard.types', string="Type")
    #Anpassungen per 09.02.2021
    rechnungsnr_eichung = fields.Char(string="Rechungsnummer")
    eichamt = fields.Text(string="Eichamt")
    letzte_eichung = fields.Date(string="letzte Eichung", default=datetime.today())
    gueltigkeit_eichung = fields.Integer(string="Gültigkeit in Jahren")
    naechste_eichung = fields.Date(string="Eichung bis", default=(datetime(datetime.today().year + 1, 12, 31)).date())
    show_user_tab_eichung = fields.Boolean(string='Show User Tab Eichung', related='category_id.show_user_tab_eichung')
    owner_user_ids = fields.Many2many('res.users', string='Owners', compute='_compute_owner_users')
    attachment_ids = fields.Many2many("ir.attachment", string="Attachments")
    attachment_count = fields.Integer(
        string="Attachments Number", compute="_compute_attachment_count"
    )
    name_seq = fields.Char(string="Nummer", default=lambda self: self._get_next_serial_no_name(),  store=True, readonly=True)
    ir_sequence_id = fields.Many2one('ir.sequence')

    def attachment_tree_view(self):
        """Get attachments for this object."""
        attachment_action = self.env.ref("base.action_attachment")
        action = attachment_action.read()[0]
        action["context"] = {
            "default_res_model": self._name,
            "default_res_id": self.ids[0],
            "no_display_create": True
        }
        action["domain"] = str(
            ["&", ("res_model", "=", self._name), ("res_id", "in", self.ids)]
        )
        return action

    @api.depends("attachment_ids")
    def _compute_attachment_count(self):
        for rec in self:
            rec.attachment_count = len(rec.env["ir.attachment"].search([("res_model", "=", self._name), ("res_id", "in", self.ids)]))

    @api.depends('customer_id', 'customer_id.street')
    def _compute_house_no(self):
        for rec in self:
            rec.house_no = ""
            rec.street = rec.customer_id.street
            if rec.customer_id and rec.customer_id.street:
                first_number = re.search('[0-9]+', rec.customer_id.street)
                if first_number:
                    first_number = re.search('[0-9]+', rec.customer_id.street).group()
                    if first_number:
                        street = rec.customer_id.street.rsplit(str(first_number), 1)[0]
                        if street:
                            rec.house_no = rec.customer_id.street.rsplit(str(street), 1)[-1]
                        rec.street = street

    @api.depends('customer_id')
    def _compute_owner_users(self):
        for rec in self:
            domain = [('type', 'not in', ['manufacturer', 'vendor'])]
            if rec.customer_id:
                owner_user_ids = rec.env['res.partner'].search([('parent_id', '=', rec.customer_id.id)])
                owners = owner_user_ids
                for owner in owner_user_ids:
                    childs = rec.env['res.partner'].search([('parent_id', '=', owner.id)])
                    while childs:
                        owners += childs
                        childs = rec.env['res.partner'].search([('parent_id', 'in', childs.ids)])
                owners += rec.customer_id
                domain = [('id', 'in', owners.mapped('user_ids').ids)]
            owners = rec.env['res.users'].search(domain)
            rec.owner_user_ids = owners.ids

    def _compute_planing_count(self):
        for equipment in self:
            equipment.planing_count = len(equipment.activity_ids)
            
    def _compute_protocol_count(self):
        for equipment in self:
            hazard.protocol_count = len(hazard.protocols_ids)
            
    def _compute_protocol_number(self):
        """Get number of protocol related to this equipment."""
        for record in self:
            record.protocol_number = self.env['hazard.protocol'].search_count([('equipment_id', '=', record.id)])

        
#     @api.onchange('category_id', 'serial_no')
#     def onchange_category_id(self):
#         if self.category_id and not self.serial_no:
#             self.name = self.category_id.name 
#         elif self.category_id and self.serial_no:
#             self.name = self.category_id.name + '/' + self.serial_no
#         elif not self.category_id and self.serial_no:
#             self.name = self.serial_no
#         else:
#             self.name = ''
            
    @api.model
    def _get_next_serial_no_name(self):
        sequence = self.env['ir.sequence'].search([('code','=','fortlaufende.seriennummer')])
        next= sequence.get_next_char(sequence.number_next_actual)
        return next
            
    @api.model
    def create(self, vals):
        if vals.get('name_seq', 'New') == 'New':
            vals['name_seq'] = self.env['ir.sequence'].next_by_code('fortlaufende.seriennummer') or 'New'
        result = super(SafetyMaster, self).create(vals)
        return result
    
    @api.onchange('category_id', 'name_seq')
    def _onchange_serial_no(self):
        if self.category_id and not self.name_seq:
            self.serial_no = self.category_id.name
        elif self.category_id and self.name_seq:
            self.serial_no = self.category_id.name + '/' + self.name_seq
        elif not self.category_id and self.name_seq:
            self.serial_no = self.name_seq
        else:
            self.serial_no = ''

#     @api.constrains('serial_no')
#     def _check_dates(self):
#         if not self.serial_no:
#             raise exceptions.ValidationError(_("Leider wurde keine Seriennummer angegeben")) 
           

class HazardCategory(models.Model):
    _name = 'hazard.category'
    _inherit = ['mail.alias.mixin', 'mail.thread']
    _description = 'Hazard Category'

    @api.depends('hazard_ids')
    def _compute_fold(self):
        # fix mutual dependency: 'fold' depends on 'equipment_count', which is
        # computed with a read_group(), which retrieves 'fold'!
        self.fold = False
        for category in self:
            category.fold = False if category.equipment_count else True

    name = fields.Char('Category Name', required=True, translate=True)
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company)
    technician_user_id = fields.Many2one('res.users', 'Responsible', tracking=True, default=lambda self: self.env.uid)
    color = fields.Integer('Color Index')
    note = fields.Text('Comments', translate=True)
    hazard_ids = fields.One2many('safety.master', 'category_id', string='Equipments', copy=False)
    equipment_count = fields.Integer(string="Equipment", compute='_compute_equipment_count')
    request_ids = fields.One2many('hazard.request', 'category_id', copy=False)
    maintenance_count = fields.Integer(string="Maintenance Count", compute='_compute_maintenance_count')
    alias_id = fields.Many2one(
        'mail.alias', 'Alias', ondelete='restrict', required=True,
        help="Email alias for this equipment category. New emails will automatically "
             "create a new equipment under this category.")
    fold = fields.Boolean(string='Folded in Maintenance Pipe', compute='_compute_fold', store=True)
    show_user_tab_eichung = fields.Boolean('Show User Tab Eichung')
    serial_no = fields.Many2one('safety.master', string='ID.')

    def _compute_equipment_count(self):
        equipment_data = self.env['safety.master'].read_group([('category_id', 'in', self.ids)],
                                                                      ['category_id'], ['category_id'])
        mapped_data = dict([(m['category_id'][0], m['category_id_count']) for m in equipment_data])
        for category in self:
            category.equipment_count = mapped_data.get(category.id, 0)

    def _compute_maintenance_count(self):
        maintenance_data = self.env['hazard.request'].read_group([('category_id', 'in', self.ids)],
                                                                      ['category_id'], ['category_id'])
        mapped_data = dict([(m['category_id'][0], m['category_id_count']) for m in maintenance_data])
        for category in self:
            category.maintenance_count = mapped_data.get(category.id, 0)

    def unlink(self):
        for category in self:
            if category.hazard_ids or category.request_ids:
                raise UserError(
                    _("You cannot delete an equipment category containing equipments or maintenance requests."))
        return super(HazardCategory, self).unlink()

    def _alias_get_creation_values(self):
        values = super(HazardCategory, self)._alias_get_creation_values()
        values['alias_model_id'] = self.env['ir.model']._get('hazard.request').id
        if self.id:
            values['alias_defaults'] = defaults = ast.literal_eval(self.alias_defaults or "{}")
            defaults['category_id'] = self.id
        return values
