# Copyright(c): 2012-Present Acespritech Solutions Pvt. Ltd.
# All Rights Reserved.
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#################################################################################

from odoo import fields, models


class FleetVehicle(models.Model):
    _inherit = 'fleet.vehicle'

    helper_id = fields.Many2one(comodel_name='res.partner', string='Helper', tracking=True,
                                help='Helper of the vehicle')

    def name_get(self):
        if self._context.get('from_picking'):
            result = [(vehicle.id, str(vehicle.license_plate)) for vehicle in self]
        else:
            result = super(FleetVehicle, self).name_get()
        return result

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4
