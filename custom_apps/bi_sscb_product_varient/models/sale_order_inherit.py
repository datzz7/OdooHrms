# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.


from odoo import fields, models, tools, api, _


class SaleOrderLineInherit(models.Model):
	_inherit = "sale.order.line"


	brand_id = fields.Many2one("custom.brand", string="Brand", copy=False)
	size_id = fields.Many2one("custom.size", string="Size", copy=False)
	style_id = fields.Many2one("custom.style", string="Style", copy=False)
	color_id = fields.Many2one("custom.color", string="Color", copy=False)


	@api.onchange('product_id')
	def product_id_change(self):
		if self.product_id:
			self.update({
					"brand_id" : self.product_id.brand_id.id,
					"size_id" : self.product_id.size_id.id,
					"style_id" : self.product_id.style_id.id,
					"color_id" : self.product_id.color_id.id,
				})
		return super(SaleOrderLineInherit, self).product_id_change()


	def write(self, vals):
		if 'product_id' in vals:
			product = self.env["product.product"].browse(vals.get('product_id', []))
			if len(product or []) != 0:
				vals.update({
					"brand_id" : product.brand_id.id,
					"size_id" : product.size_id.id,
					"style_id" : product.style_id.id,
					"color_id" : product.color_id.id,
				})

		res = super(SaleOrderLineInherit, self).write(vals)
		return res


	@api.model
	def create(self, vals):
		if 'product_id' in vals:
			product = self.env["product.product"].browse(vals.get('product_id', []))
			if len(product or []) != 0:
				vals.update({
					"brand_id" : product.brand_id.id,
					"size_id" : product.size_id.id,
					"style_id" : product.style_id.id,
					"color_id" : product.color_id.id,
				})

		res = super(SaleOrderLineInherit, self).create(vals)
		return res



class SaleReportInherit(models.Model):
	_inherit = "sale.report"


	brand_id = fields.Many2one("custom.brand", string="Brand", readonly=True)
	size_id = fields.Many2one("custom.size", string="Size", readonly=True)
	style_id = fields.Many2one("custom.style", string="Style", readonly=True)
	color_id = fields.Many2one("custom.color", string="Color", readonly=True)

	

	def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
		fields['brand_id'] = ", l.brand_id as brand_id"
		fields['size_id'] = ", l.size_id as size_id"
		fields['style_id'] = ", l.style_id as style_id"
		fields['color_id'] = ", l.color_id as color_id"
		groupby += ', l.brand_id'
		groupby += ', l.size_id'
		groupby += ', l.style_id'
		groupby += ', l.color_id'
		return super(SaleReportInherit, self)._query(with_clause, fields, groupby, from_clause)
