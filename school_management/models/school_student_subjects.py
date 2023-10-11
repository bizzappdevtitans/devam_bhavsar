from odoo import fields, models


class SchoolStudentSubjects(models.Model):
    _name = "school.student.subjects"
    _description = "Subject details"
    _rec_name = "subjects_name"

    subjects_name = fields.Char(string="Subjects")
    is_mandatory_subject = fields.Boolean(string="Mandatory subject")
    subject_teacher_ids = fields.One2many(
        comodel_name="school.teacher",
        inverse_name="subject_teacher_id",
        string="Subject Teachers",
    )
    selected_subject_ids = fields.Many2many(
        comodel_name="school.student",
        relation="student_with_subject_rel",
        column1="subjects_name",
        column2="student_first_name",
    )
