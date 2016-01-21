# b-*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (c) 2015 brain-tec AG (http://www.braintec-group.com) 
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

class Course(models.Model):
    _name = 'openacademy.course'

# Use _rec_name if there is no name field.
#    _rec_name = 'description'

    name = fields.Char(string="Course")
    description = fields.Text(string="Course Description")
    responsible_id = fields.Many2one('res.users', string="Responsible")
    session_ids = fields.One2many(comodel_name='openacademy.session', inverse_name='course_id', string="Session")

    @api.multi
    def copy(self, default):
        default = dict(default or {})
        new_name = u"Copy of {}".format(self.name)
        default['name'] = new_name
        return super(Course, self).copy(default)

    _sql_constraints = [
        ('name_description_check',
         'CHECK(name != description)',
         "The title of the course should not be the description"),

        ('name_unique',
         'UNIQUE(name)',
         "The course title must be unique"),
    ]

