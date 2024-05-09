from odoo import models, fields, api

class RegisteredName(models.Model):
    _name = 'registered.name'

    res_partner_id = fields.Many2one(comodel_name='res.partner')
    name = fields.Char(string='Registered Names')