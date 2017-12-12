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

from odoo.exceptions import ValidationError
from datetime import timedelta

from odoo import models, fields, api, _

class Session(models.Model):
    _name = 'openacademy.session'

    def _get_instructor_domain(self):
        teacher_categ_id = self.env['ir.model.data'].xmlid_to_res_id('openacademy.category_teacher')
        if teacher_categ_id:
            return ['|', ('instructor', '=', True),
                    ('category_id', 'child_of', teacher_categ_id)]
        else:
            return [('instructor', '=', True)]

    name = fields.Char(string="Session Name", required=True)
    start_date = fields.Date(string="Start Date", default=fields.Date.today)
    end_date = fields.Date(string="End Date", store=True,
                           compute='_get_end_date', inverse='_set_end_date')
    duration = fields.Integer(string="Duration in days", default=5)

    hours = fields.Float(string="Duration in hours",
                         compute='_get_hours', inverse='_set_hours')

    seats = fields.Integer(string="Number of seats", default=10)

    course_id = fields.Many2one('openacademy.course', string="Course", required=True)
    instructor_id = fields.Many2one('res.partner', string="Instructor",
                                    domain=lambda self: self._get_instructor_domain())
    attendee_ids = fields.Many2many('res.partner', string="Attendees")

    attendees_count = fields.Integer(
        string="Attendees count", compute='_get_attendees_count', store=True)

    taken_seats = fields.Float(string="Taken Seats", compute='_compute_taken_seats')
    color = fields.Integer(string="Color")
    
    state = fields.Selection([
                              ('draft', "Draft"),
                              ('confirmed', "Confirmed"),
                              ('done', "Done")
                              ], default='draft')

    @api.depends('attendee_ids')
    def _get_attendees_count(self):
        for r in self:
            r.attendees_count = len(r.attendee_ids)

    @api.depends('duration')
    def _get_hours(self):
        for r in self:
            r.hours = r.duration * 24

    def _set_hours(self):
        for r in self:
            r.duration = r.hours / 24

    @api.depends('start_date', 'duration')
    def _get_end_date(self):
        for r in self:
            if not (r.start_date and r.duration):
                r.end_date = r.start_date
                continue

            # Add duration to start_date, but: Monday + 5 days = Saturday, so
            # subtract one second to get on Friday instead
            start = fields.Datetime.from_string(r.start_date)
            duration = timedelta(days=r.duration, seconds=-1)
            r.end_date = start + duration

    def _set_end_date(self):
        for r in self:
            if not (r.start_date and r.end_date):
                continue

            # Compute the difference between dates, but: Friday - Monday = 4
            #  days, so add one day to get 5 days instead
            start_date = fields.Datetime.from_string(r.start_date)
            end_date = fields.Datetime.from_string(r.end_date)
            r.duration = (end_date - start_date).days + 1

    @api.one
    @api.depends('seats', 'attendee_ids')
    def _compute_taken_seats(self):
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
                    'title': _("Warning"),
                    'message': _("The number of seats must be above 0."),
                }

            }
        elif self.seats < len(self.attendee_ids):
            return {
                'warning': {
                    'title': _("Too many attendees"),
                    'message': _("Increase seats or remove excess attendees"),
                },
            }
        else:
            return

    @api.one
    @api.constrains('instructor_id', 'attendee_ids')
    def _check_instructor(self):
        if self.instructor_id in self.attendee_ids:
            raise ValidationError(_("Instructor of session '%s' "
                "cannot attend its own session") % self.name)

    @api.multi
    def action_confirm(self):
        self.state = 'confirmed'

    @api.multi
    def action_draft(self):
        self.state = 'draft'

    @api.multi
    def action_done(self):
        self.state = 'done'