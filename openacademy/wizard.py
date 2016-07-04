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

class Wizard(models.TransientModel):
    _name = 'openacademy.wizard'
    
    session_ids = fields.Many2many(comodel_name='openacademy.session', string="Sessions")
    attendee_ids = fields.Many2many(comodel_name='res.partner', string="Attendees")
    
    @api.multi
    def subscribe(self):
        # do something
        for session_id in self.session_ids:
            for attendee_id in self.attendee_ids:
                session_id.attendee_ids = session_id.attendee_ids + attendee_id
        return {}

