from odoo import api, fields, models


class Course(models.Model):
    _name="openacademy.course"

    name = fields.Char(string="Name of the course.", required=True)
    description = fields.Text(string="Enter a description.")
    responsible = fields.Many2one(string="Responsible for this course.", comodel_name="res.partner")
    list_of_sessions = fields.One2many(string="List of sessions for this course.", comodel_name="openacademy.session",
                                      inverse_name="related_course")