# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.


from odoo import fields, models, tools, api, _


class CustomStyle(models.Model):
	_name = "custom.style"
	_inherits = {"product.attribute.value" : "attribute_value_id"}
	_description = "Custom Style"


	attribute_value_id = fields.Many2one("product.attribute.value", string="Value")


	@api.model
	def default_get(self, fields):
		res = super(CustomStyle, self).default_get(fields)
		att_id = self.env.ref("bi_sscb_product_varient.custom_style_attr")
		if att_id:
			res["attribute_id"] = att_id.id
		return res

