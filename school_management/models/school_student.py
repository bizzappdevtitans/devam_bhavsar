from datetime import date

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SchoolStudent(models.Model):
    _name = "school.student"
    _description = "Student details"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _rec_name = "student_first_name"

    student_first_name = fields.Char(string="First Name", required=True)
    student_last_name = fields.Char(string="Last Name", required=True)
    age_of_student = fields.Integer(
        string="Age", compute="_compute_age", search="_search_age"
    )
    gender = fields.Selection(
        [("male", "Male"), ("female", "Female"), ("others", "Others")], string="Gender"
    )
    rollno = fields.Integer(string="Roll Number", required=True)
    date_of_birth = fields.Date(string="Date of birth", required=True)
    is_status_active = fields.Boolean(string="Active", default=True)
    is_confirm_info = fields.Boolean(string="Confirm Information")
    is_confirm_admission = fields.Boolean(string="Confirm Admision")
    student_photo = fields.Image(string="Student photo")
    today_date = fields.Date(string="Today")
    last_date_for_fees_payment = fields.Date(string="Last date for fees payment")
    marksheet_file = fields.Binary(string="Marksheet")
    address_student = fields.Text(string="Home Address", required=True)
    father_name_student = fields.Char(string="Father Fullname")
    mother_name_student = fields.Char(string="Mother Fullname")
    sequence_enrol_no = fields.Char(string="Sequential Enrollement number")
    standard = fields.Selection(
        [
            ("standard1", "1st"),
            ("standard2", "2nd"),
            ("standard3", "3rd"),
            ("standard4", "4th"),
            ("standard5", "5th"),
            ("standard6", "6th"),
            ("standard7", "7th"),
            ("standard8", "8th"),
            ("standard9", "9th"),
            ("standard10", "10th"),
            ("standard11", "11th"),
            ("standard12", "12th"),
        ],
        string="Standard",
        required=True,
    )
    subject_count = fields.Integer(compute="_compute_number_of_subjects")
    payment_count = fields.Integer(compute="_compute_number_of_payments")
    admission_state = fields.Selection(
        [
            ("applied", "Applied"),
            ("confirm_info", "Confirm Information"),
            ("admitted", "Admitted"),
            ("cancelled", "Cancelled"),
        ],
        string="Admission State",
        default="applied",
        tracking=True,
    )
    teacher_assigned_id = fields.Many2one(
        comodel_name="school.teacher", string="Class Teacher", tracking=True
    )
    currency_id = fields.Many2one(
        comodel_name="res.currency",
        string="Currency",
        default=lambda self: self.env.company.currency_id.id,
        required=True,
    )
    division_of_students_id = fields.Many2one(
        comodel_name="school.student.classes",
        string="Division",
        tracking=True,
    )
    subject_list_ids = fields.Many2many(
        comodel_name="school.student.subjects",
        relation="student_with_subject_rel",
        column1="student_first_name",
        column2="subjects_name",
        string="Subjects",
        tracking=True,
    )
    fees_students_ids = fields.One2many(
        comodel_name="school.student.fees",
        inverse_name="name_student_id",
        string="fees",
    )

    @api.depends("subject_list_ids")
    def _compute_number_of_subjects(self):
        """computes the number of subjects a student takes #T00335"""
        for count_of_subject in self:
            count_of_subject.subject_count = len(count_of_subject.subject_list_ids)

    def action_show_number_of_subjects(self):
        """action for smart button to show the number of subjects a student
        takes #T00335"""
        return {
            "type": "ir.actions.act_window",
            "name": "subjects",
            "view_mode": "tree",
            "res_model": "school.student.subjects",
            "domain": [("selected_subject_ids", "=", self.id)],
        }

    @api.depends("fees_students_ids")
    def _compute_number_of_payments(self):
        """computes the number of payments student made #T00335"""
        for count_of_payments in self:
            count_of_payments.payment_count = len(count_of_payments.fees_students_ids)

    def action_show_number_of_payments(self):
        """action for smart button to show the number of payments student
        made #T00335"""
        return {
            "type": "ir.actions.act_window",
            "name": "Payments",
            "view_mode": "tree,form",
            "res_model": "school.student.fees",
            "domain": [("name_student_id", "=", self.id)],
        }

    def _compute_age(self):
        """computes the age of student based on date of birth #T00335"""
        for dates in self:
            today = date.today()
            dates.age_of_student = today.year - dates.date_of_birth.year

    @api.ondelete(at_uninstall=False)
    def _unlink_check_payment(self):
        """at time of delete will check if theres any fees paid and if true then
        raise error #T00335"""
        for records in self:
            if records.fees_students_ids:
                raise ValidationError(_("Can't delete record with fees paid!"))

    @api.model
    def create(self, value):
        """Inherited create so that at time of record creation there will be a unique
        enrollement number for student #T00335"""

        value["sequence_enrol_no"] = self.env["ir.sequence"].next_by_code(
            "school.student"
        )
        return super(SchoolStudent, self).create(value)

    @api.onchange("today_date")
    def _onchange_calculate_feespayment_date(self):
        """an onchange function to calculate last fees payment date using system
        parameter #T00351"""
        month_diff = self.env["ir.config_parameter"].get_param(
            "allowed_time_period_for_feespayment"
        )
        for dates in self:
            dates.today_date = date.today()
            if dates.today_date:
                dates.last_date_for_fees_payment = dates.today_date + relativedelta(
                    months=int(month_diff)
                )

    @api.model
    def default_get(self, fields):
        """Inherited default_get so that if there are any mandatory subject they will be
        shown by default #T00335"""
        default_subjects = self.env["school.student.subjects"].search(
            [("is_mandatory_subject", "=", True)]
        )
        subjects = super(SchoolStudent, self).default_get(fields)
        subjects["subject_list_ids"] = default_subjects
        return subjects

    def archive_students_records(self):
        """server action to turn is_status_active field False and #T00404"""
        self.write({"is_status_active": False})

    def archive_record_if_in_given_states(self):
        """logic for  automated action to change a record state if state is in applied or
        admitted #T00408"""

        students = self.search(
            [
                "|",
                ("admission_state", "=", "applied"),
                ("admission_state", "=", "confirm_info"),
            ]
        )
        if students:
            students.write({"admission_state": "cancelled", "is_status_active": False})

    def _search_age(self, operator, value):
        """search method for computed field age_of_student #T00438"""
        students = self.search([]).filtered(
            lambda student: student.age_of_student == value
        )

        if not students:
            pass
        return [("id", "in", [student.id for student in students])]
