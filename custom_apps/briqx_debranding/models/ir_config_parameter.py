# -*- coding: utf-8 -*-

from odoo import models, api, tools

PARAMS = [
    'briqx_debranding.new_name',
    'briqx_debranding.new_title',
    'briqx_debranding.favicon_url',
    'briqx_debranding.planner_footer',
   
]


class IrConfigParameter(models.Model):
    _inherit = 'ir.config_parameter'

    @api.model
    @tools.ormcache()
    def get_debranding_parameters(self):
        res = {}
        for param in PARAMS:
            value = self.env['ir.config_parameter'].get_param(param)
            res[param] = value
        return res

    def write(self, vals, context=None):
        res = super(IrConfigParameter, self).write(vals)
        for r in self:
            if r.key in PARAMS:
                self.get_debranding_parameters.clear_cache(self)
                break
        return res
