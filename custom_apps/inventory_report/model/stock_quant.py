from odoo import models, fields, api, tools
from odoo.exceptions import ValidationError


class StockQuantInherit(models.Model):
    _inherit = 'stock.quant'

    internal_ref = fields.Char(related='product_id.default_code')
    case_qnty = fields.Float(compute='_compute_case_qnty_avail')
    uom_name_val =  fields.Char(related='product_id.uom_id.name')
    # inventory_quantity  = fields.Float(related = 'product_id.qty_available')
    onhand_qty_per_warehouse = fields.Float(store = True,compute = '_compute_get_onhand_qty')
    prod_name = fields.Char(comodel_name="product.product", related='product_id.name',store = True)
    product_description = fields.Char(related = 'product_id.name',store = True)
    prod_tmpl_description = fields.Char(related = 'product_tmpl_id.name')


    principal_list = []

    def _compute_get_onhand_qty(self):
        for rec in self:
            qty = rec.available_quantity + rec.reserved_quantity
            rec.onhand_qty_per_warehouse = qty

    def _compute_case_qnty_avail(self):
        for rec in self:
            qnt_pcs = rec.available_quantity

            case_uom = rec.env['uom.uom'].search([('id','=',rec.product_id.uom_po_id.id)])

            if (case_uom.uom_conversion != 0):
                res = qnt_pcs / case_uom.uom_conversion
            else:
                res = 0
            
            rec.case_qnty = res

    def return_principal_no_dup(self):
        for rec in self:
            if rec.product_id.principal.name not in self.principal_list:
                self.principal_list.append(rec.product_id.principal.name)
        sorted(self.principal_list)
   
  