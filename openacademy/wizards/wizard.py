from datetime import timedelta, datetime
from odoo.odoo.tools.misc import DEFAULT_SERVER_DATE_FORMAT

from odoo import api, fields, models, exceptions


class Wizard(models.TransientModel):
    _name="openacademy.wizard"

    sessions = fields.Many2many(string="Sessions", comodel_name="openacademy.session", relation="sessions_wizard")
    attendees = fields.Many2many(string="Attendees", comodel_name="res.partner", relation="attendees_wizard",
                                         column1="session_id", column2="partner_id")

    def _get_current_session(self):
        return self._context.get('active_id')

    @api.multi
    def save_attendees(self):
        for record in self.sessions:
            record.list_of_attendees = record.list_of_attendees | self.attendees