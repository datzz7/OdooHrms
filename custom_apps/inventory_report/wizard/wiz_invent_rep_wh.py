from odoo import models, fields, api, tools
from odoo.exceptions import ValidationError

class WizardInventoryReportWH(models.TransientModel):
    _name = 'wiz.invent.rep.wh'

    warehouse = fields.Many2one('stock.location', domain="[('location_id.name','ilike','WH')]",required=True)
    principal = fields.Many2one('res.partner')

    def action_gen(self):
        view_id = self.env.ref('inventory_report.invent_rep_view_tree').id
        domain =[]
        if self.warehouse:

            domain.append(('location_id','=',self.warehouse.id))
       
        if self.principal:
            domain.append(('principal_id','=',self.principal.id))
        return {
            'type': 'ir.actions.act_window',
            'name': 'Inventory Report per Warehouse- %s'%(self.principal.name if self.principal else ''),
            'res_model': 'stock.quant',
            'views':[(view_id,'tree')],
            'view_mode': 'tree',
            'domain': domain
       }