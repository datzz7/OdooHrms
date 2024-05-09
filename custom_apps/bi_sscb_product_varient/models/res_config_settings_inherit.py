# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.


from odoo import api, fields, models, _


class ResConfigSettingsInherit(models.TransientModel):
    _inherit = 'res.config.settings'


    def _default_style_id(self):
        md = self.env["ir.model"].search([('model','=','custom.style')])
        if md:
            return md.id
        return False

    def _default_size_id(self):
        md = self.env["ir.model"].search([('model','=','custom.size')])
        if md:
            return md.id
        return False

    def _default_color_id(self):
        md = self.env["ir.model"].search([('model','=','custom.color')])
        if md:
            return md.id
        return False

    def _domain_style_id(self):
        md = self.env["ir.model"].search([('model','=','custom.style')])
        if md:
            return "[('id','in',{})]".format(md.ids)
        return "[('id','in',[])]" 


    def _domain_size_id(self):
        md = self.env["ir.model"].search([('model','=','custom.size')])
        if md:
            return "[('id','in',{})]".format(md.ids)
        return "[('id','in',[])]"

    def _domain_color_id(self):
        md = self.env["ir.model"].search([('model','=','custom.color')])
        if md:
            return "[('id','in',{})]".format(md.ids)
        return "[('id','in',[])]"


    style_id = fields.Many2one("ir.model", string="Style", default=_default_style_id, domain=_domain_style_id)
    size_id = fields.Many2one("ir.model", string="Size", default=_default_size_id, domain=_domain_size_id)
    color_id = fields.Many2one("ir.model", string="Color", default=_default_color_id, domain=_domain_color_id)


    @api.model
    def get_values(self):
        res = super(ResConfigSettingsInherit, self).get_values()

        style_id = self.env["ir.config_parameter"].get_param("bi_sscb_product_varient.style_id")
        size_id = self.env["ir.config_parameter"].get_param("bi_sscb_product_varient.size_id")
        color_id = self.env["ir.config_parameter"].get_param("bi_sscb_product_varient.color_id")

        res.update(
            style_id = int(style_id),
            size_id = int(size_id),
            color_id = int(color_id),
        )
        return res


    def set_values(self):
        res = super(ResConfigSettingsInherit, self).set_values()

        self.env['ir.config_parameter'].set_param("bi_sscb_product_varient.style_id", self.style_id.id)
        self.env['ir.config_parameter'].set_param("bi_sscb_product_varient.size_id", self.size_id.id)
        self.env['ir.config_parameter'].set_param("bi_sscb_product_varient.color_id", self.color_id.id)



    def update_all_product_att(self):
        products = self.env["product.product"].search([("product_template_attribute_value_ids","!=",False)])
        for prd in products:
            for atrbute in prd.product_template_attribute_value_ids:
                att = atrbute.product_attribute_value_id
                if self.style_id:
                    sty = self.env["custom.style"].search([("attribute_value_id","=",att.id)])
                    if sty:
                        prd.style_id = sty.id
                        continue
                if self.size_id:
                    siz = self.env["custom.size"].search([("attribute_value_id","=",att.id)])
                    if siz:
                        prd.size_id = siz.id
                        continue
                if self.color_id:
                    colo = self.env.ref("product.product_attribute_2")
                    col = self.env["custom.color"].search([("attribute_value_id","=",att.id)])
                    if colo and att.attribute_id.id == colo.id:
                        if len(col or []) == 0:
                            col = self.env["custom.color"].create({
                                                        "attribute_value_id" : att.id,
                                                    })
                    if col:
                        prd.color_id = col.id
                        continue
