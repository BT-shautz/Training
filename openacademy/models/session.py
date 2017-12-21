from datetime import timedelta, datetime
from odoo.odoo.tools.misc import DEFAULT_SERVER_DATE_FORMAT
from odoo import _

from odoo import api, fields, models, exceptions


class Session(models.Model):
    _name = "openacademy.session"
    name = fields.Char(string="Session Name", required=True)
    start_date = fields.Date(string="Starting day of the session", default=fields.Date.today(), translate=True)
    duration = fields.Integer(string="Duration of the session (in days).")
    number_of_seats = fields.Integer(string="Amount of seats for this course.")
    related_course = fields.Many2one(string="Related course", comodel_name="openacademy.course", required=True)
    instructor = fields.Many2one('res.partner', string="Instructor",
                                domain=lambda self: self._get_instructor_domain())
    list_of_attendees = fields.Many2many(string="List of attendees", comodel_name="res.partner", relation="attendees",
                                         column1="session_id", column2="partner_id")
    percentage_taken_seats = fields.Float(string="Percentage of seats taken.", compute='_get_percentage', store=True)
    end_date = fields.Date(string="End date of the session.", compute='_get_end_date', inverse="_set_duration", store=True)
    related_course_description = fields.Text(related='related_course.description')
    color = fields.Integer(string="Color for this session.")
    duration_hours = fields.Integer(string="Duration of the session in hours.", compute='_get_duration_hours', store=True)
    total_attendees = fields.Integer(string="Total attendees of the session.", compute='_get_attendees_session', store=True)
    state = fields.Selection([('draft','Draft'), ('confirmed','Confirmed'), ('done','Done')], string="Status", default='draft')


    @api.depends('number_of_seats', 'list_of_attendees')
    def _get_percentage(self):
        for record in self:
            record.percentage_taken_seats= 100-((record.number_of_seats -
                                                 len(record.list_of_attendees))/record.number_of_seats)*100

    @api.depends('duration')
    def _get_duration_hours(self):
        for record in self:
            record.duration_hours = record.duration * 8\


    @api.depends('list_of_attendees')
    def _get_attendees_session(self):
        for record in self:
            record.total_attendees = len(record.list_of_attendees)

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

    def _get_instructor_domain(self):
        teacher_categ_id = self.env['ir.model.data'].xmlid_to_res_id('openacademy.teacher_category')
        return ['|', '&', ('category_id', '=', False), ('isInstructor', '=', True), ('category_id', 'child_of', teacher_categ_id),
                ]

    @api.onchange('number_of_seats')
    def _onchange_seats(self):

        if self.number_of_seats < 0 or self.number_of_seats < len(self.list_of_attendees):
            return {
                'warning': {
                'title': "Invalid amount of seats.",
                'message': "The amount of seats is not correct.",
        }
    }

    @api.constrains('instructor', 'list_of_attendees')
    def _constrain_instructor(self):
        for record in self:
            if record.instructor in record.list_of_attendees:
                raise exceptions.Warning("This instructor can't be on the attendee list: %s" % record.instructor)

    @api.multi
    def open_record(self):
        rec_id = self.id
        form_id = self.env.ref('openacademy.sessionViewForm')
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'openacademy.session',
            'res_id': rec_id,
            'view_type': 'form,tree',
            'view_mode': 'form',
            'view_id': form_id.id,
            'context': {},
            'target': 'current',
        }

    @api.multi
    def change_status_done(self):
        self.state = 'done'\

    @api.multi
    def change_status_confirmed(self):
        self.state = 'confirmed'

    @api.multi
    def change_status_draft(self):
        self.state = 'draft'

    @api.model
    def update_sessions(self):
        sessions = self.search([('state', '=', 'confirmed')])
        for session in sessions:
            if session.end_date > fields.Date.today():
            #if (datetime.strptime(self.end_date, DEFAULT_SERVER_DATE_FORMAT) > datetime.strptime(fields.Date.today(), DEFAULT_SERVER_DATE_FORMAT) and (self.state is 'confirmed')):
                session.state = 'done'