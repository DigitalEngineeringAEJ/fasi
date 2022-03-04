# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from dateutil.relativedelta import relativedelta
from datetime import date, datetime, timedelta

class HazardRequest(models.Model):
    _name = 'hazard.request'
    _inherit = ['mail.thread.cc', 'mail.activity.mixin']
    _description = 'Hazard Request'
    _order = "id desc"
    _check_company_auto = True

    # @api.returns('self')
    # def _default_stage(self):
    #     return self.env['maintenance.stage'].search([], limit=1)
    #
    # def _creation_subtype(self):
    #     return self.env.ref('maintenance.mt_req_created')
    #
    # def _track_subtype(self, init_values):
    #     self.ensure_one()
    #     if 'stage_id' in init_values:
    #         return self.env.ref('maintenance.mt_req_status')
    #     return super(HazardRequest, self)._track_subtype(init_values)

    def _get_default_team_id(self):
        MT = self.env['hazard.team']
        team = MT.search([('company_id', '=', self.env.company.id)], limit=1)
        if not team:
            team = MT.search([], limit=1)
        return team.id

    name = fields.Char('Subjects', required=True)
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company)
    description = fields.Text('Description')
    request_date = fields.Date('Request Date', tracking=True, default=fields.Date.context_today,
                               help="Date requested for the maintenance to happen")
    owner_user_id = fields.Many2one('res.users', string='Created by User', default=lambda s: s.env.uid)
    category_id = fields.Many2one('hazard.category', related='equipment_id.category_id',
                                  string='Category', store=True, readonly=True)
    equipment_id = fields.Many2one('safety.master', string='Equipment',
                                   ondelete='restrict', index=True, check_company=True)
    user_id = fields.Many2one('res.users', string='Technician', tracking=True)
    stage_id = fields.Many2one('maintenance.stage', string='Stage', ondelete='restrict', tracking=True)
                              # group_expand='_read_group_stage_ids', default=_default_stage, copy=False)
    priority = fields.Selection([('0', 'Very Low'), ('1', 'Low'), ('2', 'Normal'), ('3', 'High')], string='Priority')
    color = fields.Integer('Color Index')
    close_date = fields.Date('Close Date', help="Date the maintenance was finished. ")
   # kanban_state = fields.Selection(
      #  [('normal', 'In Progress'), ('blocked', 'Blocked'), ('done', 'Ready for next stage')],
        #string='Kanban State', required=True, default='normal', tracking=True)
    # active = fields.Boolean(default=True, help="Set active to false to hide the maintenance request without deleting it.")
    archive = fields.Boolean(default=False,
                             help="Set archive to true to hide the maintenance request without deleting it.")
    maintenance_type = fields.Selection([('corrective', 'Corrective'), ('preventive', 'Preventive')],
                                        string='Maintenance Type', default="corrective")
    schedule_date = fields.Datetime('Scheduled Date',
                                    help="Date the maintenance team plans the maintenance.  It should not differ much from the Request Date. ")
    maintenance_team_id = fields.Many2one('hazard.team', string='Team', required=True,
                                          default=_get_default_team_id, check_company=True)
    duration = fields.Float(help="Duration in hours.")
   # done = fields.Boolean(related='stage_id.done')

    signature = fields.Binary(string='Unterschrift Bearbeiter')
    x_garantie = fields.Boolean(string='liegt eine Garantie vor')
    x_reparatur = fields.Text('Reparatur')
    x_durchPI = fields.Text('durch PI/Region')
    x_angegebener_fehler = fields.Text('angegebener Fehler')
    date_action = fields.Datetime('Date current action', required=False, readonly=False, index=True, default=lambda self: fields.datetime.now())
    last_calibration = fields.Date(string='Letzte Kalibrierung')
    receipt_date = fields.Date(string='Eingangsdatum', default=datetime.today())
    outgoing_date = fields.Date(string='Ausgangsdatum', compute='_compute_outgoing_date')
    lead_time_manufacturer = fields.Integer(string='Tage Hersteller')
    lead_time_contractor  = fields.Integer(string='Tage Auftragnehmer', default=1)
    sum_lead_time = fields.Integer(string='Summe Durchlaufzeit', compute='_compute_sum_lead_time')
    commment = fields.Text(string='Bemerkung')
    costs_manufacturer = fields.Float(string='Kosten Hersteller')
    costs_contractor = fields.Float(string='Eigene Kosten')
    costs_parcel_service = fields.Float(string='Kosten Paketdienstleister')
    sum_costs = fields.Float(string='Summe Kosten', compute='_compute_sum_costs')
    invoice_nr = fields.Char(string='Rechnungsnummer')
    serial_no = fields.Char('Serial Number')
    pickup_address = fields.Char('Pickup Address')
    delivery_address = fields.Char('Delivery Address')
    height = fields.Float(string="Height in cm")
    width = fields.Float(string="Width in cm")
    depth = fields.Float(string="Depth in cm")
    weight = fields.Float(string="Weight in kg")

    def archive_equipment_request(self):
        self.write({'archive': True})

    def reset_equipment_request(self):
        """ Reinsert the maintenance request into the maintenance pipe in the first stage"""
        first_stage_obj = self.env['maintenance.stage'].search([], order="sequence asc", limit=1)
        # self.write({'active': True, 'stage_id': first_stage_obj.id})
        self.write({'archive': False, 'stage_id': first_stage_obj.id})

    @api.onchange('company_id')
    def _onchange_company_id(self):
        if self.company_id and self.maintenance_team_id:
            if self.maintenance_team_id.company_id and not self.maintenance_team_id.company_id.id == self.company_id.id:
                self.maintenance_team_id = False

    @api.onchange('equipment_id')
    def onchange_equipment_id(self):
        if self.equipment_id:
            self.user_id = self.equipment_id.technician_user_id if self.equipment_id.technician_user_id else self.equipment_id.category_id.technician_user_id
            self.category_id = self.equipment_id.category_id
            if self.equipment_id.maintenance_team_id:
                self.maintenance_team_id = self.equipment_id.maintenance_team_id.id

    @api.onchange('category_id')
    def onchange_category_id(self):
        if not self.user_id or not self.equipment_id or (self.user_id and not self.equipment_id.technician_user_id):
            self.user_id = self.category_id.technician_user_id

    @api.model
    def create(self, vals):
        # context: no_log, because subtype already handle this
        request = super(HazardRequest, self).create(vals)
        if request.owner_user_id or request.user_id:
            request._add_followers()
        if request.equipment_id and not request.maintenance_team_id:
            request.maintenance_team_id = request.equipment_id.maintenance_team_id
        request.activity_update()
        return request

#     def write(self, vals):
#         # Overridden to reset the kanban_state to normal whenever
#         # the stage (stage_id) of the Maintenance Request changes.
#         if vals and 'kanban_state' not in vals and 'stage_id' in vals:
#             vals['kanban_state'] = 'normal'
#         res = super(HazardRequest, self).write(vals)
#         if vals.get('owner_user_id') or vals.get('user_id'):
#             self._add_followers()
#         if 'stage_id' in vals:
#             self.filtered(lambda m: m.stage_id.done).write({'close_date': fields.Date.today()})
#             self.activity_feedback(['maintenance.mail_act_maintenance_request'])
#         if vals.get('user_id') or vals.get('schedule_date'):
#             self.activity_update()
#         if vals.get('equipment_id'):
#             # need to change description of activity also so unlink old and create new activity
#             self.activity_unlink(['maintenance.mail_act_maintenance_request'])
#             self.activity_update()
#         return res

    def activity_update(self):
        """ Update maintenance activities based on current record set state.
        It reschedule, unlink or create maintenance request activities. """
        self.filtered(lambda request: not request.schedule_date).activity_unlink(
            ['maintenance.mail_act_maintenance_request'])
        for request in self.filtered(lambda request: request.schedule_date):
            date_dl = fields.Datetime.from_string(request.schedule_date).date()
            updated = request.activity_reschedule(
                ['maintenance.mail_act_maintenance_request'],
                date_deadline=date_dl,
                new_user_id=request.user_id.id or request.owner_user_id.id or self.env.uid)
            if not updated:
                if request.equipment_id:
                    note = _('Request planned for <a href="#" data-oe-model="%s" data-oe-id="%s">%s</a>') % (
                        request.equipment_id._name, request.equipment_id.id, request.equipment_id.display_name)
                else:
                    note = False
                request.activity_schedule(
                    'maintenance.mail_act_maintenance_request',
                    fields.Datetime.from_string(request.schedule_date).date(),
                    note=note, user_id=request.user_id.id or request.owner_user_id.id or self.env.uid)

    def _add_followers(self):
        for request in self:
            partner_ids = (request.owner_user_id.partner_id + request.user_id.partner_id).ids
            request.message_subscribe(partner_ids=partner_ids)

    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        """ Read group customization in order to display all the stages in the
            kanban view, even if they are empty
        """
        stage_ids = stages._search([], order=order, access_rights_uid=SUPERUSER_ID)
        return stages.browse(stage_ids)

    @api.constrains('lead_time_contractor')
    def _compute_sum_lead_time(self):
        for record in self:
            self.sum_lead_time = self.lead_time_manufacturer + self.lead_time_contractor
    
    @api.constrains('sum_lead_time')
    def _compute_outgoing_date(self):
        if self.sum_lead_time:
            for record in self:
                self.outgoing_date = self.receipt_date + relativedelta(days=self.sum_lead_time)
        else: 
            self.outgoing_date = self.date_action.now()
            
    @api.constrains('costs_contractor')
    def _compute_sum_costs(self):
        for record in self:
            self.sum_costs = self.costs_manufacturer + self.costs_contractor + self.costs_parcel_service
            
    # --------
    
    #@api.onchange('kanban_state')
    #def action_generate_protocol_rep(self):
    @api.onchange('equipment_id', 'request_date')
    def onchange_equipmentid(self):
        if self.equipment_id.serial_no and self.request_date:
            self.serial_no = self.equipment_id.serial_no
            self.name = self.serial_no  + '_' + str(self.request_date.strftime('%d/%m/%y'))

    name = fields.Char(string='Name')
    
    def action_generate_protocol_rep(self):
        protocol_vals = {
            'name': self.equipment_id.name,
            'category_id':self.category_id.name,
            'description':self.description,
            'signature': self.signature,
            'x_garantie':self.x_garantie,
            'x_reparatur':self.x_reparatur,
            'x_durchPI':self.x_durchPI,
            'x_angegebener_fehler':self.x_angegebener_fehler,
            'order_date':self.request_date,
            'date':self.schedule_date,
            'serial_no':self.env['safety.master'].search([('id', '=', self.equipment_id.id)]).serial_no,
            'manufacturer_id':self.env['safety.master'].search([('id', '=', self.equipment_id.id)]).manufacturer_id.id,
            'customer_id':self.env['safety.master'].search([('id', '=', self.equipment_id.id)]).customer_id.id,
            'contractor_id':self.env['safety.master'].search([('id', '=', self.equipment_id.id)]).technician_user_id.id,
            'equipment_service_id':self.env['hazard.service'].search([('name','=',"Reparatur")]).id,
            'maintenance_request_id':self.id,
            'equipment_id': self.equipment_id.id if self.equipment_id else False
            #'equipment_service_id':3 --> So wäre das richtig schlecht programmmiert --> Hardcode Pfui!!!!!
            }
        history_vals = { 
        'name': self.equipment_id.id,
        'current_date': self.date_action.now(),
        'topic': 'Reparatur Protokoll erstellt',
        'request_id': self.id,
            }
        
        protocol = self.env['hazard.protocol'].create(protocol_vals)
        history = self.env['hazard.history'].create(history_vals)
        
    @api.onchange('stage_id')
    def action_generate_history_vals(self): 
        history_vals2 = {
        'name': self.equipment_id.id,
        'current_date': self.date_action.now(),
        'topic': self.stage_id.name,
        'request_id':self.id,
          }
        history2 = self.env['hazard.history'].create(history_vals2)