from datetime import date

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SchoolStudentFees(models.Model):
    _name = "school.student.fees"
    _description = "Student Fees details"
    _rec_name = "name_student_id"

    currency_id = fields.Many2one(
        comodel_name="res.currency",
        string="Currency",
        store=True,
        default=lambda self: self.env.user.company_id.currency_id.id,
    )
    name_student_id = fields.Many2one(comodel_name="school.student", string="Name")
    paid_date = fields.Date(string="Date of Payment", store=True, default=date.today())
    paid_fees = fields.Monetary(string="Paid fees", store=True)
    total_fees = fields.Monetary(string="Total fees", default="5000")
    remaning_fees = fields.Monetary(
        string="Remaining fees",
        compute="_compute_student_fees",
    )

    @api.onchange("paid_fees", "total_fees", "remaning_fees")
    def _compute_student_fees(self):
        """calculate student fees and if given invalid details raise error #T00335"""
        for payments in self:
            if payments.paid_fees <= payments.total_fees:
                payments.remaning_fees = payments.total_fees - payments.paid_fees
            elif payments.remaning_fees < 0:
                raise ValidationError(_("Please enter proper information"))
