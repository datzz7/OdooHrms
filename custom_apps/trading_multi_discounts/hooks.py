# -*- encoding: utf-8 -*-

from odoo import SUPERUSER_ID
from odoo import api


def post_init_hook(cr, registry):
    """
    website menu hide
    """
    env = api.Environment(cr, SUPERUSER_ID, {})
    cr.execute("""
                update ir_model_data set noupdate=False where
                model ='ir.rule' """)