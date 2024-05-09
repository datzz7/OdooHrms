from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    sale_type = fields.Selection(string='Type', selection=[('sale', 'Sale'), ('project', 'Project')], default='sale', required=True)
    
    @api.model
    def create(self, vals):
        context = self._context
        default_sale_type = context.get('default_sale_type')
        if default_sale_type == 'project':
            if vals.get("name", "New") == "New":
                # Find the sequence record with the name 'seq_project_sale_order'
                sequence = self.env["ir.sequence"].search([('name', '=', 'project_sale_qoutation')],limit=1)
                # if sequence:
                    # If the sequence exists, generate the next sequence number
                name = sequence.next_by_id()
                vals['name'] = name
                # else:
                #     # If the sequence doesn't exist, create it
                #     sequence = self.env["ir.sequence"].create({
                #         'name': 'Project Sale Quotation',
                #         'code': 'sale.order',
                #         'prefix': 'PSQ-',
                #         'padding': 5,
                #         'number_next': 1,
                #         'number_increment': 1,
                #     })
                #     vals['name'] = sequence.next_by_id()
        return super(SaleOrder, self).create(vals)
