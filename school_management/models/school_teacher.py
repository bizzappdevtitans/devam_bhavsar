from datetime import date, datetime

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SchoolTeacher(models.Model):
    _name = "school.teacher"
    _description = "Teacher details"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _rec_name = "first_name"

    first_name = fields.Char(string=" First Name", required=True)
    last_name = fields.Char(string="Last Name", required=True)
    age_teacher = fields.Integer(string="Age", compute="_compute_age", store=True)
    sequence_teacher_number = fields.Char(string="Sequential teacher number")
    gender = fields.Selection(
        [("male", "Male"), ("female", "Female"), ("others", "Others")], string="Gender"
    )
    date_of_birth = fields.Date(string="Date of birth", required=True)
    is_status_active = fields.Boolean(string="Active", default=True, tracking=True)
    teacher_photo = fields.Image(
        string="Teacher photo",
    )
    email_teacher = fields.Char(string="email")
    student_count = fields.Integer(compute="_compute_number_of_students")
    assigned_student_ids = fields.One2many(
        comodel_name="school.student",
        inverse_name="teacher_assigned_id",
        string="Students",
    )
    assigned_supervisor_id = fields.Many2one(
        comodel_name="school.supervisor", string="Supervisor", tracking=True
    )
    phone_no_teacher = fields.Integer(string="Phone number")
    subject_teacher_id = fields.Many2one(
        comodel_name="school.student.subjects", string="Subject", tracking=True
    )

    @api.depends("date_of_birth")
    def _compute_age(self):
        """computes the age of teacher based on date of birth #T00335"""
        for dates in self:
            todate = date.today()
            if dates.date_of_birth:
                dates.age_teacher = todate.year - dates.date_of_birth.year

    @api.depends("assigned_student_ids")
    def _compute_number_of_students(self):
        """computes the number of student a teacher has #T00335"""
        for count_of_student in self:  # counts the number of students
            count_of_student.student_count = len(count_of_student.assigned_student_ids)

    def action_show_number_of_students(self):
        """action for smart button to show the number of student a teacher has #T00335"""
        return {
            "type": "ir.actions.act_window",
            "name": "Students",
            "view_mode": "tree,form",
            "res_model": "school.student",
            "domain": [("teacher_assigned_id", "=", self.id)],
            "context": "",
            "target": "current",
        }

    @api.constrains("phone_no_teacher")
    def _validate_phone_no_teacher(self):
        """validates teacher phone number #T00335"""
        for digits in self:
            # checks if phone is inputed or not if true checks the length anf if more
            # than 10 raise error
            if digits.phone_no_teacher and len(digits.phone_no_teacher) != 10:
                raise ValidationError(
                    _("enter Phone number and number should not exceed 10 digits")
                )

    @api.model
    def create(self, value):
        """Inherited create so that at time of record creation there will be a unique
        employee number for teacher #T00335"""
        value["sequence_teacher_number"] = self.env["ir.sequence"].next_by_code(
            "school.teacher"
        )
        return super(SchoolTeacher, self).create(value)

    def action_find_and_wish_birthday(self):
        """action of cron job to search and find teachers whose birthday is today and
        wish them happy bday in birthday channel #T00398"""
        dates = self.search(
            [("date_of_birth", "ilike", datetime.today().strftime("%m-%d"))]
        )
        teacher_birthday = dates.filtered(
            lambda names_of_teacher: names_of_teacher.first_name
        ).mapped("first_name")
        if teacher_birthday:
            msg = "Happy Birthday to", " ".join(teacher_birthday)
            self.env["mail.message"].create(
                {
                    "email_from": self.env.user.partner_id.email,
                    "author_id": self.env.user.partner_id.id,
                    "model": "mail.channel",
                    "message_type": "comment",
                    "subtype_id": self.env["ir.model.data"]._xmlid_to_res_id(
                        "mail.mt_comment"
                    ),
                    "body": " ".join(msg),
                    "res_id": self.env.ref(
                        "school_management.school_teacher_birthday_announcements"
                    ).id,
                }
            )
