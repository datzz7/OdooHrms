from odoo import _, api, fields, models
from odoo.exceptions import UserError



class InheritSaleReport(models.Model):
    _inherit = 'sale.report'
    _auto = False

    prod_division_id  = fields.Many2one(comodel_name='product.attr.division', string='Product Division')
    prod_department_id  = fields.Many2one(comodel_name='product.attr.department', string='Product Department')
    
    def _select_sale(self, fields=None):
        return super(InheritSaleReport,self)._select_sale()+'''
        ,t.product_division_id as prod_division_id
        ,t.product_department_id as prod_department_id'''
    
    def _from_sale(self, from_clause=''):
        return super(InheritSaleReport,self)._from_sale()+'''
        left join product_attr_division padiv on t.product_division_id = padiv.id
        left join product_attr_department padav on t.product_department_id = padav.id
'''
        
    
    def _group_by_sale(self, groupby=''):
        return super(InheritSaleReport,self)._group_by_sale()+'''
        ,t.product_division_id,t.product_department_id
'''