from datetime import date

from dateutil.relativedelta import relativedelta

from odoo.tests.common import TransactionCase


class TestSchoolStudentClasses(TransactionCase):
    def setUp(self):
        """Created a payment and student record #T00475"""
        super(TestSchoolStudentClasses, self).setUp()
        self.class_1 = self.env["school.student.classes"].create(
            {
                "division": "divisionA",
            }
        )
        self.student_1 = self.env["school.student"].create(
            {
                "student_first_name": "Test1",
                "student_last_name": "Test1",
                "rollno": 1,
                "date_of_birth": date.today() - relativedelta(years=15),
                "address_student": "TEST",
                "standard": "standard1",
                "division_of_students_id": self.class_1.id,
            }
        )

    def test_compute_number_of_students(self):
        """tests compute_number_of_students method #T00475"""
        self.assertEqual(
            self.class_1.student_count,
            len(self.class_1.class_students_ids),
            "number of students dosent match student count of a class",
        )

    def test_action_show_number_of_students(self):
        """Tests if the students ids are in the smart button #T00475"""
        self.assertIn(
            self.class_1.class_students_ids.division_of_students_id.id,
            [
                students
                for classes in self.class_1.action_show_number_of_students().get(
                    "domain"
                )
                for students in classes
            ],
        )
