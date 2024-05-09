from odoo import fields, api, models, _


class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    