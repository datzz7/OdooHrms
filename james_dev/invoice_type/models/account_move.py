from odoo import _, api, fields, models
from odoo.exceptions import ValidationError



class InheritAccountMove(models.Model):
    _inherit = 'account.move'

    invoice_type = new_field = fields.Selection(selection=[('tra', 'Trust Receipt Agreement'), ('csi', 'Charge Sales Invoice'),('csinv','Cash Sales Invoice')])
    
