from odoo import _, api, fields, models
from odoo.exceptions import UserError



class InheritProductTemplate(models.Model):
    _inherit = 'product.template'
    
    product_division_id  = fields.Many2one(comodel_name='product.attr.division')
    product_department_id  = fields.Many2one(comodel_name='product.attr.department')
    
    
    # def write(self, vals):
    #     if 'product_division_id' in vals:
    #         raise UserError("You are not allowed to update the related_model_id field.")
    #     return super(InheritProductTemplate, self).write(vals)