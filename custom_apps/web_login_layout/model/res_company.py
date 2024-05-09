from odoo import fields, models

class ResCompany(models.Model):
    _inherit = "res.company"

    bg_image = fields.Many2one('ir.attachment',string="Background Image",help="Attach Background Image")
    bg_color = fields.Char('Background Color')
    bg_blur = fields.Integer('Background Blur')
    
    layout_option = fields.Selection([(' ','Default'),('l1','Style 1'),('l2','Style 2'),('l3','Style 3'),('l4','Style 4')],string="Template", default='l3')
    layout_structure = fields.Char('Layout Structure')