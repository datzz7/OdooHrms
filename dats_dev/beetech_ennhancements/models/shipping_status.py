# -*- code: utf-8 -*-

from odoo import fields, api, models, _


class ShippingStatus(models.Model):
    _name = 'po.shipping.status'
    _description = 'Sequence for shipping status'
    _rec_name = 'status'
    _sql_constraints = [
        (
            "unique_sequence_no",
            "unique(sequence_no)",
            "Sequence number already taken."
        )
    ]
    
    
    sequence_no = fields.Char(string="Sequence", required=True)
    status = fields.Char(string="Status")