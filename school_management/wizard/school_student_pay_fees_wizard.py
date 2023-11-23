from datetime import date

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class StudentPayfeesWizard(models.TransientModel):
    _name = "student.payfees.wizard"
    _description = "student pay fees"
    currency_id = fields.Many2one(
        comodel_name="res.currency",
        string="Currency",
        store=True,
        default=lambda self: self.env.user.company_id.currency_id.id,
    )
    name_student = fields.Many2one(
        comodel_name="school.student",
        string="Name",
        default=lambda self: self._default_student_name(),
    )
    paid_date = fields.Date(string="Date of Payment", store=True, default=date.today())
    paid_fees = fields.Monetary(string="Paid fees", store=True)
    total_fees = fields.Monetary(string="Total fees")
    remaning_fees = fields.Monetary(
        string="Remaining fees",
    )

    @api.onchange("name_student", "paid_fees")
    def _onchange_student_fees(self):
        """calculate student fees and if given invalid details raise error #T00335"""
        if self.name_student.standard == "standard1":
            for payments in self:
                payments.total_fees = self.env["ir.config_parameter"].get_param(
                    "1st_standard_fees"
                )
                payments.remaning_fees = payments.total_fees - payments.paid_fees
                if payments.remaning_fees < 0:
                    raise ValidationError(_("Please enter proper information"))

    def action_pay_fees(self):
        """when clicked submit this will create a record in school.student.fees
        model with values inputed from wizard #T00348"""
        return self.env["school.student.fees"].create(
            {
                "name_student_id": self.name_student.id,
                "paid_date": self.paid_date,
                "paid_fees": self.paid_fees,
                "total_fees": self.total_fees,
                "remaning_fees": self.remaning_fees,
                "currency_id": self.currency_id.id,
            }
        )

    @api.model
    def _default_student_name(self):
        """fucntion to get default name of student in wizard #T00348"""
        context = dict(self._context) or {}
        student_name = self.env["school.student"].browse(
            context.get("active_id", False)
        )
        return student_name and student_name.id
