# -*- coding: utf-8 -*-

from odoo import models, fields, api


class KsRmaLine(models.Model):
    _inherit = "ks.rma.line"
    
    
    lot_id = fields.Many2one(comodel_name='stock.production.lot',string="Lot/Serial No")
    check_tracking = fields.Boolean(compute='_get_product_tracking')
    
    
    @api.depends('ks_product_id')
    def _get_product_tracking(self):
        for rec in self:
            if rec.ks_product_id:
                rec.check_tracking = False if rec.ks_product_id.tracking == 'none' else True