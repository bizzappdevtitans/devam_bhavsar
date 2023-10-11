from odoo import fields, models


class SchoolStudentClasses(models.Model):
    _name = "school.student.classes"
    _description = "Class details"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _rec_name = "division"

    strength_of_class = fields.Integer(string="Strength of class")
    class_standard = fields.Selection(
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
    )
    division = fields.Selection(
        selection=[
            ("divisionA", "A"),
            ("divisionB", "B"),
            ("divisionC", "C"),
            ("divisionD", "D"),
        ],
        string="Division",
    )
    class_teacher_id = fields.Many2one(
        comodel_name="school.teacher", string="Class Teacher", tracking=True
    )
    class_students_ids = fields.One2many(
        comodel_name="school.student",
        inverse_name="division_of_students_id",
        string="Students",
        tracking=True,
    )
    student_count = fields.Integer(compute="_compute_number_of_students")

    def _compute_number_of_students(self):
        """computes the number of students in a class for smart button #T00335"""
        for count_of_student in self:
            count_of_student.student_count = self.env["school.student"].search_count(
                [("division_of_students_id", "=", count_of_student.id)]
            )

    def action_show_number_of_students(self):
        """action of smart button to show number of students #T00335"""
        return {
            "type": "ir.actions.act_window",
            "name": "Students",
            "view_mode": "tree,form",
            "res_model": "school.student",
            "domain": [("division_of_students_id", "=", self.id)],
            "context": "",
            "target": "current",
        }
