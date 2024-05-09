# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.


from odoo import fields, models, tools, api, _


class CustomBrand(models.Model):
	_name = "custom.brand"
	_description = "Custom Brand"


	name = fields.Char(string="Brand", required=True)

