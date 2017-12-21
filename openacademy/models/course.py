from odoo import api, fields, models


class Course(models.Model):
    _name="openacademy.course"
    _sql_constraints=[('name_dif', 'CHECK(name != description)',  'The name and the description must be different!'),
                      ('name_uniq', 'UNIQUE (name)', 'Course name must be unique!')]

    name = fields.Char(string="Name of the course.", required=True)
    description = fields.Text(string="Enter a description.")
    responsible = fields.Many2one(string="Responsible for this course.", comodel_name="res.users")
    list_of_sessions = fields.One2many(string="List of sessions for this course.", comodel_name="openacademy.session",
                                       inverse_name="related_course")

    @api.multi
    def copy(self, default=None):
        if default is None:
            default = {}
        if 'name' in default:
            default['name'] = "Copy of " + default['name']
        else:
            default['name'] = "Copy of " + self.name
        res = super(Course, self).copy(default=default)
        return res