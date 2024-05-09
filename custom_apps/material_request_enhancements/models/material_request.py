from odoo import models, fields, api, _
from odoo.exceptions import UserError


class MaterialRequest(models.Model):
    _inherit = 'material.request'

    request_type = fields.Selection(
        selection_add=[('goods_issue', "Goods Issue")])
    search_ids = fields.Char(
        compute="_compute_search_ids", search='search_ids_search')
    name = fields.Char(string='Request No', readonly=True,
                       copy=False, default="New")
    assigned_to = fields.Many2one('res.users', 'Approver',
                                  required=True, )
    back_order_id = fields.Many2one(
        comodel_name='material.request', string="Reference")
    analytic_accounts = fields.Many2one(
        comodel_name='account.analytic.account', string="Analytic")
    analytic_tag_ids = fields.Many2many(
        comodel_name='account.analytic.tag', string="Analytic Tags")
    currency_id = fields.Many2one(
        comodel_name='res.currency', related='company_id.currency_id')
    req_type = fields.Selection(
        [('rfq', 'RFQ'), ('purchase', 'Purchase Order'), ('goods_issue', "Goods Issue")], 'Acquire Method', store=True)

    @api.onchange('analytic_accounts')
    def _onchange_analytic_accounts(self):
        for rec in self.line_ids:
            rec.update({'account_analytic_id': self.analytic_accounts,
                        'analytic_tag_ids': [(6, 0, self.analytic_tag_ids.ids)]})
    
    
    @api.onchange('req_type')
    def onchange_req_type(self):
        self.request_type = self.req_type
        if self.request_type == 'rfq' or self.request_type == 'purchase' or self.request_type == 'tender':
            self.picking_type_id = self.get_picking_type('incoming')
        if self.request_type == 'transfer':
            self.picking_type_id = self.get_picking_type('internal')
        if self.request_type == 'manufacture':
            self.picking_type_id = self.get_picking_type('mrp_operation')

    # override request type
    @api.onchange('request_type')
    def onchange_request_type(self):
        res = super(MaterialRequest, self).onchange_request_type()
        if self.request_type == 'goods_issue':
            self.picking_type_id = self.get_picking_type('outgoing')

        return res


    def make_approved(self):
        view_wiz_id = self.env.ref(
            'material_request_enhancements.check_availability_wizard_form')
        counter = 0
        for rec in self:
            for line in rec.line_ids:
                if line.approved_qty > 0.0:
                    counter += 1
                if line.approved_qty > line.product_qty:
                    raise UserError(
                        _("Material cleared qty must not be greater than product qty. !"))
            # if counter == 0 and rec.request_type == 'goods_issue':
            #     raise UserError('You are trying to clear 0 qty. Please check cleared qty or change acquire method to RFQ.')

            if rec.request_type == 'goods_issue':
                if rec.state != 'approved':
                    for line in rec.line_ids:
                        if line.product_qty != line.approved_qty:
                            return {
                                'type': 'ir.actions.act_window',
                                'res_model': 'create.requisition',
                                'view_mode': 'form',
                                'view_type': 'form',
                                'action_id': 'check_availability_action_wizard_confirm',
                                'view_id': view_wiz_id.id,
                                'target': 'new',
                            }
            rec.state = 'approved'
        res = super(MaterialRequest, self).make_approved()
        return res


class MaterialRequestLine(models.Model):
    _inherit = 'material.request.line'

    balance = fields.Float(string='Balance', compute='compute_balance')
    account_analytic_id = fields.Many2one(comodel_name='account.analytic.account', string='Analytic Account', default='account_analytic_id')
    analytic_tag_ids = fields.Many2many(comodel_name='account.analytic.tag', column1='mrline_id',
                                                column2='analytic_tag_ids', relation='material_request_line_analytic_tag_rel', default='analytic_tag_ids')
    uom_id = fields.Many2one(comodel_name='uom.uom', string="Unit of Measure")
    
    @api.depends('product_qty', 'approved_qty')
    def compute_balance(self):
        for rec in self:
            rec.balance = rec.product_qty - rec.approved_qty

    