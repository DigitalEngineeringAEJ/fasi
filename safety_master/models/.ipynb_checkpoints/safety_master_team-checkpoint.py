import ast

from datetime import date, datetime, timedelta

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import UserError
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT


class HazardTeam(models.Model):
    _name = 'hazard.team'
    _description = 'Hazard Teams'

    name = fields.Char('Team Name', required=True, translate=True)
    active = fields.Boolean(default=True)
    company_id = fields.Many2one('res.company', string='Company',
        default=lambda self: self.env.company)
    member_ids = fields.Many2many(
        'res.users', 'maintenance_team_users_rel', string="Team Members",
        domain="[('company_ids', 'in', company_id)]")
    color = fields.Integer("Color Index", default=0)
    request_ids = fields.One2many('hazard.request', 'maintenance_team_id', copy=False)
    equipment_ids = fields.One2many('safety.master', 'maintenance_team_id', copy=False)

    # For the dashboard only
#     todo_request_ids = fields.One2many('hazard.request', string="Requests", copy=False, compute='_compute_todo_requests')
#     todo_request_count = fields.Integer(string="Number of Requests", compute='_compute_todo_requests')
#     todo_request_count_date = fields.Integer(string="Number of Requests Scheduled", compute='_compute_todo_requests')
#     todo_request_count_high_priority = fields.Integer(string="Number of Requests in High Priority", compute='_compute_todo_requests')
#     todo_request_count_block = fields.Integer(string="Number of Requests Blocked", compute='_compute_todo_requests')
#     todo_request_count_unscheduled = fields.Integer(string="Number of Requests Unscheduled", compute='_compute_todo_requests')

    @api.depends('request_ids.stage_id.done')
    def _compute_todo_requests(self):
        for team in self:
            team.todo_request_ids = self.env['hazard.request'].search([('maintenance_team_id', '=', team.id), ('stage_id.done', '=', False)])
            team.todo_request_count = len(team.todo_request_ids)
            team.todo_request_count_date = self.env['hazard.request'].search_count([('maintenance_team_id', '=', team.id), ('schedule_date', '!=', False)])
            team.todo_request_count_high_priority = self.env['hazard.request'].search_count([('maintenance_team_id', '=', team.id), ('priority', '=', '3')])
            team.todo_request_count_block = self.env['hazard.request'].search_count([('maintenance_team_id', '=', team.id), ('kanban_state', '=', 'blocked')])
            team.todo_request_count_unscheduled = self.env['hazard.request'].search_count([('maintenance_team_id', '=', team.id), ('schedule_date', '=', False)])

    @api.depends('equipment_ids')
    def _compute_equipment(self):
        for team in self:
            team.equipment_count = len(team.equipment_ids)