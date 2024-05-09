# -*- coding: utf-8 -*-

from odoo import _, api, models


class HrPayslip(models.Model):
    _inherit = "hr.payslip"

    def button_import_attendance(self):
        for payslip in self:
            payslip._import_attendance()

    def _import_attendance(self):
        self.ensure_one()
        wd_obj = self.env["hr.payslip.worked_days"]
        day_obj = self.env["hr.attendance"]
        date_from = self.date_from
        date_to = self.date_to

        criteria1 = [
            ("payslip_id", "=", self.id),
            ("import_from_attendance", "=", True),
        ]
        wd_obj.search(criteria1).unlink()

        res = {
            "name": _("Total Attendance"),
            "code": "ATTN",
            "number_of_days": 0.0,
            "number_of_hours": 0.0,
            "contract_id": self.contract_id.id,
            "import_from_attendance": True,
            "payslip_id": self.id,
        }

        criteria2 = [
            ("check_in", ">=", date_from),
            ("check_out", "<=", date_to),
            ("employee_id", "=", self.employee_id.id),
            # ("sheet_id.state", "=", "done"),
        ]

        for day in day_obj.search(criteria2):
            res["number_of_days"] += 1
            res["number_of_hours"] += day.worked_hours

        wd_obj.create(res)
