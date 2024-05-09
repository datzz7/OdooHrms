# -*- coding: utf-8 -*-

import datetime
from odoo import api, fields, models, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.exceptions import UserError


class InventoryAdjustment(models.Model):
	_inherit = 'stock.inventory'

	force_date = fields.Datetime(string="Force Date")

class StockPicking(models.Model):
	_inherit = 'stock.picking'

	force_date = fields.Datetime(string="Force Date")


class StockMove(models.Model):
	_inherit = 'stock.move'

	force_date = fields.Datetime(string="Force Date",compute='_compute_force_date', store=True)

	@api.depends('picking_id.force_date','inventory_id.force_date')
	def _compute_force_date(self):
		for rec in self:
			if rec.picking_id:
				rec.force_date = rec.picking_id.force_date
			elif rec.inventory_id:
				rec.force_date = rec.inventory_id.force_date
     
     
	def _action_done(self, cancel_backorder=False):
		if self.env.user.has_group('stock_force_date_app.group_stock_force_date'):
			force_date = ''
			for move in self:
				force_date = move.force_date
				if move.picking_id:
					if move.picking_id.force_date:
						force_date = move.picking_id.force_date
					else:
						force_date = move.picking_id.scheduled_date
				if move.inventory_id:
					if move.inventory_id.force_date:
						force_date = move.inventory_id.force_date
					else:
						force_date = move.inventory_id.date

		res = super(StockMove, self)._action_done(cancel_backorder=cancel_backorder)
		if self.env.user.has_group('stock_force_date_app.group_stock_force_date'):
			if res.picking_id.force_date or res.inventory_id.force_date:
				for move in res:
					force_date = move.force_date
					move.write({'date':move.force_date})
					if move.stock_valuation_layer_ids:
						for stock_v in move.stock_valuation_layer_ids:
							stock_v.write({'create_date':move.force_date})
							self.env.cr.execute(
									"UPDATE stock_valuation_layer SET create_date = %s WHERE id = %s",
										[move.force_date, stock_v.id])
					if move.move_line_ids:
						for move_line in move.move_line_ids:
							move_line.write({'date':move.force_date})
					if move.account_move_ids:
						for account_move in move.account_move_ids:
							self.env.cr.execute(
									"UPDATE account_move SET date = %s WHERE id = %s",
										[move.force_date, account_move.id])
							if account_move.line_ids:
								for line in account_move.line_ids:
									line.write({'date':move.force_date})

		return res


	def _create_account_move_line(self, credit_account_id, debit_account_id, journal_id, qty, description, svl_id, cost):
		self.ensure_one()
		AccountMove = self.env['account.move'].with_context(default_journal_id=journal_id)

		move_lines = self._prepare_account_move_line(qty, cost, credit_account_id, debit_account_id, description)
		if move_lines:
			date = self._context.get('force_period_date', fields.Date.context_today(self))
			if self.env.user.has_group('stock_force_date_app.group_stock_force_date'):
				if self.picking_id.force_date:
					date = self.picking_id.force_date.date()
			new_account_move = AccountMove.sudo().create({
				'journal_id': journal_id,
				'line_ids': move_lines,
				'date': date,
				'ref': description,
				'stock_move_id': self.id,
				'stock_valuation_layer_ids': [(6, None, [svl_id])],
				'move_type': 'entry',
			})
			new_account_move._post()


class StockQuant(models.Model):
	_inherit = 'stock.quant'

	force_date = fields.Datetime(string="Force Date")

	@api.model
	def _get_inventory_fields_write(self):
		""" Returns a list of fields user can edit when he want to edit a quant in `inventory_mode`.
		"""
		return ['inventory_quantity','force_date']

	def _get_inventory_move_values(self, qty, location_id, location_dest_id, out=False):
		res = super(StockQuant, self)._get_inventory_move_values(qty, location_id, location_dest_id, out=False)
		if res:
			if self.force_date:
				res.update({
					'date': self.force_date,
					'force_date': self.force_date,
				})
		return res

	def write(self, vals):
		""" Override to handle the "inventory mode" and create the inventory move. """
		allowed_fields = self._get_inventory_fields_write()
		if self._is_inventory_mode() and any(field for field in allowed_fields if field in vals.keys()):
			if any(quant.location_id.usage == 'inventory' for quant in self):
				# Do nothing when user tries to modify manually a inventory loss
				return
			if not self.env.user.has_group('stock_force_date_app.group_stock_force_date'):
				if any(field for field in vals.keys() if field not in allowed_fields):
					raise UserError(_("Quant's editing is restricted, you can't do this operation."))
			self = self.sudo()
			return super(StockQuant, self).write(vals)
		return super(StockQuant, self).write(vals)


class AccountMove(models.Model):
	_inherit = 'account.move'

	@api.constrains('name', 'journal_id', 'state')
	def _check_unique_sequence_number(self):
		moves = self.filtered(lambda move: move.state == 'posted')
		if not moves:
			return

		self.flush(['name', 'journal_id', 'move_type', 'state'])
		if not self.env.user.has_group('stock_force_date_app.group_stock_force_date'):
			# /!\ Computed stored fields are not yet inside the database.
			self._cr.execute('''
				SELECT move2.id, move2.name
				FROM account_move move
				INNER JOIN account_move move2 ON
					move2.name = move.name
					AND move2.journal_id = move.journal_id
					AND move2.move_type = move.move_type
					AND move2.id != move.id
				WHERE move.id IN %s AND move2.state = 'posted'
			''', [tuple(moves.ids)])
			res = self._cr.fetchall()
			if res:
				raise ValidationError(_('Posted journal entry must have an unique sequence number per company.\n'
										'Problematic numbers: %s\n') % ', '.join(r[1] for r in res))