from odoo import _, api, fields, models



class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    purchase_type  = fields.Selection(string='Type', selection=[('purchase', 'Purchase'), ('project', 'Project')], default= 'purchase',required=True)