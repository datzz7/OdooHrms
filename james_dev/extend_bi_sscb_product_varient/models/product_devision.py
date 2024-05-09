from odoo import _, api, fields, models
from odoo.exceptions import UserError



class ProductAttrDivision(models.Model):
    _name = 'product.attr.division'
    _description = 'Product Attribute Division'

    name  = fields.Char(string='Devision')
    
