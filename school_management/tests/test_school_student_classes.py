from datetime import date

from dateutil.relativedelta import relativedelta

from odoo.tests.common import TransactionCase


class TestSchoolStudentClasses(TransactionCase):
    def setUp(self):
        """Created a payment and student record #T00475"""
        self.student_1 = self.env["school.student"].create(
            {
                "student_first_name": "Test1",
                "student_last_name": "Test1",
                "rollno": 1,
                "date_of_birth": date.today() - relativedelta(years=15),
                "address_student": "TEST",
                "standard": "standard1",
            }
        )
        self.class_1 = self.env["school.student.classes"].create(
            {
                "class_students_ids": self.student_1.ids,
            }
        )

        super(TestSchoolStudentClasses, self).setUp()

    def test_compute_number_of_students(self):
        """tests compute_number_of_students method #T00475"""
        self.assertEqual(
            self.class_1.student_count, len(self.class_1.class_students_ids), "Fail"
        )

    def test_action_show_number_of_students(self):
        """tests action_show_number_of_students method #T00475"""
        self.class_1.action_show_number_of_students()
