# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    tin_no = fields.Char(string="TIN",)
    project_details = fields.Text(string="Project / Order info")
    
    @api.onchange('partner_id')
    def _get_partner_tin(self):
        if self.partner_id:
            self.tin_no = self.partner_id.vat
        else:
            self.tin_no = None

    @api.model
    def create(self, vals):
        pricelist = vals.get('pricelist_id')
        pricelist = self.env['product.pricelist'].search([('id','=',pricelist)]).name
        if pricelist == 'Project':
            if vals.get("name", "New") == "New":
                # Find the sequence record with the name 'seq_project_sale_order'
                sequence = self.env["ir.sequence"].search([('name', '=', 'project_sale_qoutation')],limit=1)
                name = sequence.next_by_id()
                vals['name'] = name
              
        return super(SaleOrder, self).create(vals)