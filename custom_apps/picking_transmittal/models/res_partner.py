# -*- coding: utf-8 -*-


from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    salesman_id = fields.Many2one(comodel_name='res.users', string='Salesman',
                                default=lambda self: self.env.user)
    encoder_id = fields.Many2one(comodel_name='res.users', string='Encoder',
                                default=lambda self: self.env.user)
