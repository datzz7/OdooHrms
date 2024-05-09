# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.


from odoo import fields, models, tools, api, _


class ProductTemplateInherit(models.Model):
	_inherit = "product.template"


	brand_id = fields.Many2one("custom.brand", string="Brand", copy=False)




class ProductProductInherit(models.Model):
	_inherit = "product.product"


	size_id = fields.Many2one("custom.size", string="Size", copy=False)
	style_id = fields.Many2one("custom.style", string="Style", copy=False)
	color_id = fields.Many2one("custom.color", string="Color", copy=False)


	@api.model
	def create(self, vals):
		res = super(ProductProductInherit, self).create(vals)
		for rec in res:
			varr = self.env["product.template.attribute.value"]
			try:
				varr = self.env["product.template.attribute.value"].browse(vals.get("product_template_attribute_value_ids")[0][2] or [])
			except:
				pass 
			if len(varr or []) != 0:
				for atrbute in varr:
					att = atrbute.product_attribute_value_id 

					sty = self.env["custom.style"].search([("attribute_value_id","=",att.id)])
					if sty:
						rec.style_id = sty.id
						continue
					siz = self.env["custom.size"].search([("attribute_value_id","=",att.id)])
					if siz:
						rec.size_id = siz.id
						continue

					colo = self.env.ref("product.product_attribute_2")
					col = self.env["custom.color"].search([("attribute_value_id","=",att.id)])
					if colo and att.attribute_id.id == colo.id:
						if len(col or []) == 0:
							col = self.env["custom.color"].create({
														"attribute_value_id" : att.id,
													})
					if col:
						rec.color_id = col.id
						continue
		return res

	

	def name_get(self):
		res = super(ProductProductInherit, self).name_get()
		values = []
		for lt in res:
			prd = self.env["product.product"].browse(lt[0])
			if prd.brand_id or prd.color_id or prd.style_id or prd.size_id:
				atr = " ".join([prd.brand_id.name or '', prd.color_id.name or '', 
							prd.style_id.name or '', prd.size_id.name or ''])
			else:
				atr = ""
			ind = lt[1].find(']')
			if ind != -1:
				if len(atr):
					lt1 = lt[1][:ind+1] + " [{}] ".format(atr) + lt[1][ind+1:]
				else:
					lt1 = lt[1]
			else:
				if len(atr):
					lt1 = "[{}] ".format(atr) + lt[1]
				else:
					lt1 = lt[1]

			values.append((lt[0], lt1))

		return values