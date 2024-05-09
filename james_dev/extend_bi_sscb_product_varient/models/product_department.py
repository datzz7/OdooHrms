from odoo import _, api, fields, models
from odoo.exceptions import UserError



class ProductAttrDepartment(models.Model):
    _name = 'product.attr.department'
    _description = 'Product Attribute Department'


    name = fields.Char(string='Department')
    
