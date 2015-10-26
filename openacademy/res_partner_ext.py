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

from openerp import api, models, fields

class Partner(models.Model):
    _inherit = 'res.partner'
    
    instructor = fields.Boolean(string="Is an instructor?")
    name_candidate = fields.Char(string="Name of the candidate", required=True)
    address_candidate = fields.Char(string="Address of the candidate", required=True)
    
    @api.one
    def _assign_address(self):
        
        self.addressCandidate = "Calle Velazquez"
    
    @api.model
    def _add_data_partner(self):
        """ 
        Assign values to demo mandatory fields within res.partner
        """
        # Find records with empty firstname and lastname
        partners_null = self.search([("address_candidate", "=", False)])

        # Force calculations there
        partners_null._assign_address()
