# b-*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (c) 2015 brain-tec AG (http://www.brain-tec.ch)
#    All Right Reserved
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields, api
from openerp.exceptions import ValidationError

class Session(models.Model):
    _name = 'openacademy.session'

    active = fields.Boolean(string="Active", default=True)
    name = fields.Char(string="Session Name", required=True)
    start_date = fields.Date(string="Start Date", default=fields.Date.today)
    duration = fields.Integer(string="Duration in days", default=5)
    seats = fields.Integer(string="Number of seats", default=20)
    instructor_id = fields.Many2one(string="Instructor", comodel_name='res.users', domain=[('is_instructor', '=', True)])
    course_id = fields.Many2one(string="Course", comodel_name='openacademy.course') 
    attendee_ids = fields.Many2many(string="Attendees", comodel_name='res.partner')
    taken_seats = fields.Float(string="Taken Seats", compute='_compute_taken_seats', store=True)
    color = fields.Integer(string="Color")
    state = fields.Selection([('draft', "Draft"),
                              ('confirmed', "Confirmed"),
                              ('done', "Done")],
                              default='draft')
    
    @api.one
    def action_draft(self):
        self.state = 'draft'

    @api.one
    def action_confirm(self):
        self.state = 'confirmed'

    @api.one
    def action_done(self):
        self.state = 'done'

    @api.constrains('attendee_ids', 'instructor_id')
    def _check_instructor_not_in_attendees(self):
        if self.instructor_id.partner_id in self.attendee_ids:
            raise ValidationError("The instructor can not attend his own session: %s"
                                  % self.instructor_id.partner_id.name )

    @api.onchange('seats', 'attendee_ids')
    def _onchange_seats_attendees(self):
        if self.seats < len(self.attendee_ids):
            return {
                    'warning' : {
                                 'title' : "Warning",
                                 'message': "There are more attendees than seats!"
                                 }
                    }

    @api.depends('seats', 'attendee_ids')
    def _compute_taken_seats(self):
        for session in self:
            print "Seats: ", session.seats
            print "Attendees: ", session.attendee_ids
            if session.seats == 0:
                session.taken_seats = 0
            else:
                session.taken_seats = 100 * len(session.attendee_ids) / session.seats


