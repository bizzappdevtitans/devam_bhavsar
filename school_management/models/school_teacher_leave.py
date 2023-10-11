from dateutil.relativedelta import relativedelta

from odoo import api, fields, models


class SchoolTeacherLeave(models.Model):
    _name = "school.teacher.leave"
    _description = "Teacher Leave details"
    _rec_name = "teacher_name_id"

    teacher_name_id = fields.Many2one(
        comodel_name="school.teacher", string="Teacher name"
    )
    leave_date_from = fields.Date(string="Leave from", required=True)
    leave_date_to = fields.Date(string="Leave to", required=True)
    total_days = fields.Integer(
        string="Total days",
        compute="_compute_total_days",
        inverse="_inverse_calculate_date_from_total_days",
        required=True,
    )
    leave_reason = fields.Text(string="Leave reason")
    leave_types = fields.Selection(
        [
            ("medical_leave ", "Medical leave"),
            ("casual_leave", "Casual leave"),
            ("unpaid_leave", "Unpaid leave"),
        ]
    )

    @api.onchange("leave_date_to", "leave_date_from")
    def _compute_total_days(self):
        """compute method to count total leave days based on leave_from and leave_to
        #T00435"""
        for dates in self:
            if dates.leave_date_from and dates.leave_date_to:
                dates.total_days = (dates.leave_date_to - dates.leave_date_from).days

    @api.onchange("total_days", "leave_date_from")
    def _inverse_calculate_date_from_total_days(self):
        """Inverse of compute method to set leave_date_to from leave_date_from and
        total_days #T00435"""
        for dates in self:
            if dates.leave_date_from and dates.total_days:
                dates.leave_date_to = dates.leave_date_from + relativedelta(
                    days=dates.total_days
                )
