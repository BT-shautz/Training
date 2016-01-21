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

from openerp.exceptions import ValidationError

from openerp import models, fields, api

class Session(models.Model):
    _name = 'openacademy.session'

    name = fields.Char(string="Session Name", required=True)
    start_date = fields.Date(string="Start Date", default=fields.Date.today)
    duration = fields.Integer(string="Duration in days", default=5)
    seats = fields.Integer(string="Number of seats", default=10)

    course_id = fields.Many2one('openacademy.course', string="Course", required=True)
    instructor_id = fields.Many2one('res.partner', string="Instructor", domain="[('instructor', '=', True)]")
    attendee_ids = fields.Many2many('res.partner', string="Attendees")

    taken_seats = fields.Float(string="Taken Seats", compute='_compute_taken_seats')
    color = fields.Integer(string="Color")
    
    state = fields.Selection([
                              ('draft', "Draft"),
                              ('confirmed', "Confirmed"),
                              ('done', "Done")
                              ], default='draft')

    @api.one
    @api.depends('seats', 'attendee_ids')
    def _compute_taken_seats(self):
        print "Session:", self.name
        print "User:", self.env.user.name
        if not self.seats:
            self.taken_seats = 0.0
        else:
            self.taken_seats = 100.0 * len(self.attendee_ids) / self.seats
        return

    @api.onchange('seats')        
    def _check_seats(self):
        if self.seats <= 0:
            return {
                'warning' : {
                    'title': "Warning",
                    'message': "The number of seats must be above 0.",
                }

            }
        else:
            return

    @api.one
    @api.constrains('instructor_id', 'attendee_ids')
    def _check_instructor(self):
        if self.instructor_id in self.attendee_ids:
            raise ValidationError("Instructor of session '%s' "
                "cannot attend its own session" % self.name)

    @api.multi
    def action_confirm(self):
        self.state = 'confirmed'

    @api.multi
    def action_draft(self):
        self.state = 'draft'

    @api.multi
    def action_done(self):
        self.state = 'done'