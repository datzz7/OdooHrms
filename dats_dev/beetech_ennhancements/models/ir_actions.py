from odoo import models, fields, api, _, tools

class irActions(models.Model):
    _inherit = 'ir.actions.actions'
    
    @api.model
    @tools.ormcache('frozenset(self.env.user.groups_id.ids)', 'model_name')
    def get_bindings(self, model_name):
        res = super(irActions, self).get_bindings(model_name)
        actions = res.get('action')
        if actions:
            for action in actions:
                if action.get('name') == "Register Payment":
                    actions.remove(action)
                    res.update({'action': actions})
        
        return res