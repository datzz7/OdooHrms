# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrderType(models.Model):
    _name = 'sales.order.type'
    _description = "Sales Order Type"

    

    name = fields.Char()
    code = fields.Char()