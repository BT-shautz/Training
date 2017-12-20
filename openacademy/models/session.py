from datetime import timedelta, datetime
from odoo.odoo.tools.misc import DEFAULT_SERVER_DATE_FORMAT

from odoo import api, fields, models


class Session(models.Model):
    _name = "openacademy.session"
    name = fields.Char(string="Session Name", required=True)
    start_date = fields.Date(string="Starting day of the session", default=fields.Date.today())
    duration = fields.Integer(string="Duration of the session (in days).")
    number_of_seats = fields.Integer(string="Amount of seats for this course.")
    related_course = fields.Many2one(string="Related course", comodel_name="openacademy.course", required=True)
    instructor = fields.Many2one(string="Instructor", comodel_name="res.partner")
    list_of_attendees = fields.Many2many(string="List of attendees", comodel_name="res.partner", relation="attendees",
                                         column1="session_id", column2="partner_id")
    percentage_taken_seats = fields.Float(string="Percentage of seats taken.", compute='_get_percentage')
    end_date = fields.Date(string="End date of the session.", compute='_get_end_date', inverse="_set_duration")
    related_course_description = fields.Text(related='related_course.description')

    @api.depends('number_of_seats', 'list_of_attendees')
    def _get_percentage(self):
        for record in self:
            record.percentage_taken_seats= 100-((record.number_of_seats -
                                                 len(record.list_of_attendees))/record.number_of_seats)*100

    @api.depends('start_date', 'duration')
    def _get_end_date(self):
        for record in self:
            record.end_date = datetime.strftime(datetime.strptime(record.start_date, DEFAULT_SERVER_DATE_FORMAT) +
                                                timedelta(days=record.duration), DEFAULT_SERVER_DATE_FORMAT)

    def _set_duration(self):
        for record in self:
            if not (record.start_date and record.duration):
                continue
            record.duration = (datetime.strptime(record.end_date, DEFAULT_SERVER_DATE_FORMAT) -
                               datetime.strptime(record.start_date, DEFAULT_SERVER_DATE_FORMAT)).days