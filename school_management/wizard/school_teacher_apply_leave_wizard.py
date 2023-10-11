from dateutil.relativedelta import relativedelta

from odoo import api, fields, models


class SchoolTeacherLeaveWizard(models.TransientModel):
    _name = "school.teacher.leave.wizard"
    _description = "Teacher Leave Wizard"

    teacher_name_id = fields.Many2one(
        comodel_name="school.teacher",
        string="Name",
        default=lambda self: self._default_teacher_name(),
    )
    leave_date_from = fields.Date(string="Leave from", required=True)
    leave_date_to = fields.Date(string="Leave to", required=True)
    leave_reason = fields.Text(string="Leave reason")
    total_days = fields.Integer(
        string="Total days",
        compute="_compute_total_days",
        inverse="_inverse_calculate_date_from_total_days",
        required=True,
    )
    leave_type = fields.Selection(
        [
            ("medical_leave ", "Medical leave"),
            ("casual_leave", "Casual leave"),
            ("unpaid_leave", "Unpaid leave"),
        ]
    )

    def action_apply_leave(self):
        """when clicked submit this will create a record in school.teacher.leave
        model with values inputed from wizard #T00348 action for wizard"""
        return self.env["school.teacher.leave"].create(
            {
                "teacher_name_id": self.teacher_name_id.id,
                "leave_types": self.leave_type,
                "leave_date_from": self.leave_date_from,
                "leave_date_to": self.leave_date_to,
                "total_days": self.total_days,
                "leave_reason": self.leave_reason,
            }
        )

    @api.model
    def _default_teacher_name(self):
        """function to get default name of teacher in wizard #T00348"""
        context = dict(self._context) or {}
        teacher_name = self.env["school.teacher"].browse(
            context.get("active_id", False)
        )
        return teacher_name and teacher_name.id

    @api.onchange("leave_date_to", "leave_date_from")
    def _compute_total_days(self):
        """compute method to count total leave days based on leave_date_from and
        leave_date_to #T00435"""
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
