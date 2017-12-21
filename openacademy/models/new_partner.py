from odoo import api, fields, models


class NewPartner(models.Model):
    _inherit = "res.partner"

    isInstructor = fields.Boolean(string="Is an instructor?")
    partner_session_relation = fields.Many2many(string="Relationship between partner and session.",
                                                comodel_name="openacademy.session", relation="relationship_partner_session",
                                                column1="partner_id", column2="session_id")
