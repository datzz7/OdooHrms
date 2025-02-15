import base64
import json
import math
import re

from werkzeug import urls

from odoo import fields as odoo_fields, http, tools, _, SUPERUSER_ID
from odoo.exceptions import ValidationError, AccessError, MissingError, UserError
from odoo.http import content_disposition, Controller, request, route
from odoo.tools import consteq



class CustomerPortal(Controller):

    MANDATORY_BILLING_FIELDS = ["name", "phone", "email", "street", "city", "country_id"]
    OPTIONAL_BILLING_FIELDS = ["zipcode", "state_id", "vat", "company_name"]

    _items_per_page = 20

    

 #    def _prepare_portal_layout_values(self):
 #        """Values for /my/* templates rendering.

 #        Does not include the record counts.
 #        """
 #        # get customer sales rep
 #        sales_user = False
 #        partner = request.env.user.partner_id
 #        if partner.user_id and not partner.user_id._is_public():
 #            sales_user = partner.user_id

 #        return {
 #            'sales_user': sales_user,
 #            'page_name': 'home',
 #            'archive_groups': [],
 #        }

	# @route(['/my/account'], type='http', auth='user', website=True)
 #    def account(self, redirect=None, **post):
 #        values = self._prepare_portal_layout_values()
 #        partner = request.env.user.partner_id
 #        values.update({
 #            'error': {},
 #            'error_message': [],
 #        })

 #        if post and request.httprequest.method == 'POST':
 #            error, error_message = self.details_form_validate(post)
 #            values.update({'error': error, 'error_message': error_message})
 #            values.update(post)
 #            if not error:
 #                values = {key: post[key] for key in self.MANDATORY_BILLING_FIELDS}
 #                values.update({key: post[key] for key in self.OPTIONAL_BILLING_FIELDS if key in post})
 #                for field in set(['country_id', 'state_id']) & set(values.keys()):
 #                    try:
 #                        values[field] = int(values[field])
 #                    except:
 #                        values[field] = False
 #                values.update({'zip': values.pop('zipcode', '')})
 #                partner.sudo().write(values)
 #                if redirect:
 #                    return request.redirect(redirect)
 #                return request.redirect('/my/home')

 #        countries = request.env['res.country'].sudo().search([])
 #        states = request.env['res.country.state'].sudo().search([])

 #        values.update({
 #            'partner': partner,
 #            'countries': countries,
 #            'states': states,
 #            'has_check_vat': hasattr(request.env['res.partner'], 'check_vat'),
 #            'redirect': redirect,
 #            'page_name': 'my_details',
 #        })

 #        response = request.render("portal.portal_my_details", values)
 #        response.headers['X-Frame-Options'] = 'DENY'
 #        return response