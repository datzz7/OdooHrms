from odoo import models

class InheritProudctTemplate(models.Model):
    _inherit = 'product.template'


    def print_product_count_sheet(self):
        report_action = self.env.ref('modify_odoo_reports.action_report_product_list_countsheet')
        report = report_action.report_action(self)
        return report
