from odoo import api, fields, models

class ResConfigSettingsLys(models.TransientModel):
    _inherit = 'res.config.settings'
    
    bg_image = fields.Many2one('ir.attachment', related="company_id.bg_image", string="Background Image",help="Attach background Image", readonly=False)
    bg_color = fields.Char(related="company_id.bg_color", string='Background Color', readonly=False)
    bg_blur = fields.Integer(related="company_id.bg_blur", string='Background Blur', readonly=False)
    
    layout_option = fields.Selection([(' ','Default'),('l1','Style 1'),('l2','Style 2'),('l3','Style 3'),('l4','Style 4')], related="company_id.layout_option", string="Template", readonly=False)
    layout_structure = fields.Char(related="company_id.layout_structure", string='Layout Structure', readonly=False)
    
    @api.onchange('layout_option')
    def _layout_option(self):
        if self.layout_option == 'l1':
            self.layout_structure = 'lys_layout1'
        elif self.layout_option == 'l2':
            self.layout_structure = 'lys_layout2'
        elif self.layout_option == 'l3':
            self.layout_structure = 'lys_layout3'
        elif self.layout_option == 'l4':
            self.layout_structure = 'lys_layout4'
        else:    
            self.layout_structure = 'o_home_menu_background'

    def execute(self):
        res = super(ResConfigSettingsLys, self).execute()
        self.ensure_one()
        return res
