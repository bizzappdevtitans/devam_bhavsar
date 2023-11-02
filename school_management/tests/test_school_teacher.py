from datetime import date

from dateutil.relativedelta import relativedelta

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestSchoolTeacher(TransactionCase):
    def setUp(self):
        """Created a teacher and two student records #T00475"""
        self.teacher_1 = self.env["school.teacher"].create(
            {
                "first_name": "test_first_name",
                "last_name": "test_last_name",
                "date_of_birth": date.today() - relativedelta(years=25),
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
                "teacher_assigned_id": self.teacher_1.id,
            }
        )
        self.student_2 = self.env["school.student"].create(
            {
                "student_first_name": "Test2",
                "student_last_name": "Test2",
                "rollno": 2,
                "date_of_birth": date.today() - relativedelta(years=15),
                "address_student": "TEST2",
                "standard": "standard1",
                "teacher_assigned_id": self.teacher_1.id,
            }
        )
        super(TestSchoolTeacher, self).setUp()

    def test_compute_number_of_students(self):
        """tests compute_number_of_students method #T00475"""
        self.assertEqual(
            len(self.teacher_1.assigned_student_ids),
            self.teacher_1.student_count,
            "Fail",
        )

    def test_action_show_number_of_students(self):
        """tests action_show_number_of_students #T00475"""
        self.teacher_1.action_show_number_of_students()

    def test_validate_phone_no_teacher(self):
        """tests validate_phone_no_teacher method #T00475"""
        with self.assertRaises(ValidationError):
            self.teacher_1.write({"phone_no_teacher": 333333})

    def test_action_find_and_wish_birthday(self):
        """tests action_find_and_wish_birthday method #T00475"""
        self.teacher_1.action_find_and_wish_birthday()
