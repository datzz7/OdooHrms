from odoo import models, fields, api, _
from odoo.exceptions import UserError

class CreateRequisition(models.TransientModel):
    _inherit = 'create.requisition'
    
    def auto_create_rfq_material(self):
        name_seq = ''
        prod_to_rfq = 0
        mri_balance = self.env['material.request']
        mri_lines = self.env['material.request.line']
        Purchase = self.env['purchase.order']
        PurchaseLine = self.env['purchase.order.line']
        order_lines = self.env['purchase.order.line']
        context = dict(self._context or {})
        def_supplier = self.env['res.partner'].search([('name', 'ilike', 'Default Supplier')])
        active_id = context.get('active_id', []) or []
        if context.get('active_model') == 'material.request' and active_id:
            request_rec = self.env['material.request'].browse(active_id)
            if request_rec:
                name_seq = self.env['ir.sequence'].next_by_code('material.request')
                    
                draft_po_id = Purchase.create({
                    'partner_id': def_supplier.id,
                    'notes': request_rec.note or "",
                    'origin': request_rec.name or "",
                    'material_request_id': request_rec.id or "",
                    'analytic_accounts': request_rec.analytic_accounts.id
                })
                mri_balance_id = mri_balance.create({
                            'name': name_seq,
                            'back_order_id': request_rec.id,
                            'state': 'approved',
                            'request_type': request_rec.request_type,
                            'assigned_to': request_rec.assigned_to.id,
                            'analytic_accounts': request_rec.analytic_accounts.id,
                            'picking_type_id': request_rec.picking_type_id.id
                            })
                if draft_po_id:
                    for line in request_rec.line_ids:
                        name = line.description or ""
                        if line.product_id:
                            name = line.product_id.name
                            if line.product_id.code:
                                name = '[%s] %s' % (name, line.product_id.code)
                        if line.product_qty != line.approved_qty:
                            prod_to_rfq = line.product_qty - line.approved_qty
                            order_lines |= PurchaseLine.create(
                                        {
                                            'product_id': line.product_id.id,
                                            'name': name,
                                            'product_qty': prod_to_rfq,
                                            'product_uom': line.product_uom_id.id,
                                            'date_planned': fields.Datetime.now(),
                                            'account_analytic_id': request_rec.analytic_accounts.id,
                                            'price_unit': 0.0,
                                            'order_id': draft_po_id and draft_po_id.id or False
                                        })
                            
                            mri_lines.create({
                                'material_id': mri_balance_id.id,
                                'product_id': line.product_id.id,
                                'description': name,
                                'product_qty': line.balance,
                                'approved_qty': line.balance,
                                'product_uom_id': line.product_uom_id.id,    
                            })
                        
                        for rec in request_rec:
                            rec.state = 'approved'
                            
                                
                    draft_po_id.order_line = [(6, 0, order_lines.ids)]
                    return draft_po_id
    
    def proceed(self):
        context = dict(self._context or {})
        active_id = context.get('active_id', []) or []
        mri_ids = self.env['material.request'].browse(active_id)
        for rec in mri_ids:
            rec.state = 'approved'
        return True

    def create_purchase_record(self):
        Purchase = self.env['purchase.order']
        PurchaseLine = self.env['purchase.order.line']
        order_lines = self.env['purchase.order.line']
        if not self.partner_id:
            raise UserError(_("Please select supplier !"))
        context = dict(self._context or {})
        active_id = context.get('active_id', []) or []
        if context.get('active_model') == 'material.request' and active_id:
            request_rec = self.env['material.request'].browse(active_id)
            if request_rec:
                draft_po_id = Purchase.create({
                    'partner_id': self.partner_id.id,
                    'notes': request_rec.note or "",
                    'origin': request_rec.name or "",
                    'account_analytic_id': request_rec.analytic_accounts.id,
                    'analytic_tag_ids': [(6, 0, request_rec.analytic_tag_ids.ids)]
                })
                if draft_po_id:
                    for line in request_rec.line_ids:
                        if line.approved_qty <= 0.0:
                            raise UserError(_("Material approved qty must be positive !"))
                        name = line.description or ""
                        order_lines |= PurchaseLine.create(
                                    {
                                        'product_id': line.product_id.id,
                                        'name': name,
                                        'product_qty': line.approved_qty,
                                        'product_uom': line.uom_id.id,
                                        'date_planned': fields.Datetime.now(),
                                        'price_unit': 0.0,
                                        'order_id': draft_po_id and draft_po_id.id or False,
                                        'analytic_tag_ids': [(6,0, line.analytic_tag_ids.ids)],
                                        'account_analytic_id': line.account_analytic_id.id
                                    })
                    draft_po_id.order_line = [(6, 0, order_lines.ids)]
                    return draft_po_id