# -*- coding: utf-8 -*-

from odoo import fields, models


class HrPayslipWorkedDays(models.Model):
    _inherit = "hr.payslip.worked_days"

    import_from_attendance = fields.Boolean(
        string="Imported From Timesheet",
        default=False,
    )
