from odoo import fields, models, api
import logging
_logger = logging.getLogger(__name__)



class StockQuant(models.Model):
    _inherit = 'stock.quant'
    
    
    direct_price_unit = fields.Float(compute="return_direct_price",store = True)
    route_price_uniit = fields.Float(compute="return_route_price",store = True)
    total_price_onhand_direct_price = fields.Float(compute="compute_onhand_direct_price")
    total_price_onhand_route_price = fields.Float(compute="compute_onhand_route_price")

    @api.depends("product_tmpl_id","product_id")
    def return_direct_price(self):
        for rec in self:    
            pro_tmp = rec.env['product.template'].search([('id','=',rec.product_id.id)]) 
            dp_val = rec.env["product.pricelist.item"].search([('pricelist_id','=',21),('product_tmpl_id','=',pro_tmp.id)])  
            
            if dp_val:
                rec.direct_price_unit = dp_val.fixed_price
            else:
                rec.direct_price_unit = 0

    @api.depends("product_tmpl_id","product_id")
    def return_route_price(self):
        for rec in self:    
            pro_tmp = rec.env['product.template'].search([('id','=',rec.product_id.id)]) 
            dp_val = rec.env["product.pricelist.item"].search([('pricelist_id','=',19),('product_tmpl_id','=',pro_tmp.id)])  
          
            if dp_val:
                rec.route_price_uniit = dp_val.fixed_price
            else:
                rec.route_price_uniit = 0


    def compute_onhand_direct_price(self):
        for rec in self:
            total = rec.inventory_quantity * rec.direct_price_unit
            if total:
                rec.total_price_onhand_direct_price = total
            else:
                rec.total_price_onhand_direct_price = 0

    def compute_onhand_route_price(self):
        for rec in self:
            total = rec.inventory_quantity * rec.route_price_uniit
            if total:
                rec.total_price_onhand_route_price = total
            else:
                rec.total_price_onhand_route_price = 0


    
           
       