# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    _sql_constraints = [
        ('customer_po_no_uniq' , 'unique (customer_po_no)', 'Customer PO number must be unique!')
    ]
    
    salesman_id = fields.Many2one(comodel_name='res.users', domain=[('is_salesman', '=', True)], required=True, tracking=True)
    customer_po_no = fields.Char(string="PO Number", tracking=True, copy=False)
    order_type = fields.Many2one(comodel_name='sales.order.type', string="Order Type", required=True, tracking=True)
    country_id = fields.Many2one(comodel_name='sales.area', string="Area", required=True,)
    vat = fields.Char(string="VAT", tracking=True)
    partner_registered_names = fields.Many2one(comodel_name='registered.name', copy=False)
    
    
    # override create function: contains all custom logic
    @api.model
    def create(self, vals):
        res = super(SaleOrder, self).create(vals)
        
        
        return res
    
    @api.onchange('partner_id')
    def _onchange_partner_id_vat_change(self):
        for rec in self:
            if rec.partner_id:
                rec.vat = rec.partner_id.vat
                
                return {'domain': {'partner_registered_names': [('res_partner_id', '=', rec.partner_id.id)]}}
            else:
                rec.vat = None
                return
                