from datetime import date

from dateutil.relativedelta import relativedelta

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestSchoolStudent(TransactionCase):
    def setUp(self):
        """Created a student,class,payments records and two subject records #T00475"""
        self.subject_1 = self.env["school.student.subjects"].create(
            {"subjects_name": "Maths"}
        )
        self.subject_2 = self.env["school.student.subjects"].create(
            {"subjects_name": "Science"}
        )
        self.payment_1 = self.env["school.student.fees"].create({"paid_fees": 200})
        self.class_1 = self.env["school.student.classes"].create(
            {"division": "divisionA"}
        )
        self.student_1 = self.env["school.student"].create(
            {
                "student_first_name": "Test1",
                "student_last_name": "Test1",
                "rollno": 1,
                "date_of_birth": date.today() - relativedelta(years=15),
                "address_student": "TEST",
                "standard": "standard1",
                "subject_list_ids": [
                    (6, 0, [self.subject_2.id, self.subject_1.id]),
                ],
                "fees_students_ids": [
                    (6, 0, [self.payment_1.id]),
                ],
                "division_of_students_id": self.class_1.id,
            }
        )
        super(TestSchoolStudent, self).setUp()

    def test_compute_age(self):
        """tests the compute age method #T00475"""
        self.assertEqual(self.student_1.age_of_student, 15, "Fail")

    def test_compute_number_of_subjects(self):
        """tests the subject count compute method #T00475"""
        self.assertEqual(
            len(self.student_1.subject_list_ids), self.student_1.subject_count, "Fail"
        )
        self.student_1.action_show_number_of_subjects()

    def test_compute_number_of_payments(self):
        """tests the payment count compute method #T00475"""
        self.assertEqual(
            len(self.student_1.fees_students_ids), self.student_1.payment_count, "Fail"
        )
        self.student_1.action_show_number_of_payments()

    def test_unlink_check_payment(self):
        """test if validation error is raised when deleteing a record #T00475"""
        with self.assertRaises(ValidationError):
            self.student_1.unlink()

    def test_onchange_calculate_feespayment_date(self):
        """tests _onchange_calculate_feespayment_date method #T00475"""
        self.student_1._onchange_calculate_feespayment_date()
        month_diff = self.env["ir.config_parameter"].get_param(
            "allowed_time_period_for_feespayment"
        )
        self.assertEqual(
            self.student_1.last_date_for_fees_payment,
            self.student_1.today_date + relativedelta(months=int(month_diff)),
            "Fail",
        )

    def test_search_age(self):
        """tests search_age method #T00475"""
        # case:1 the method returns empty list #T00475
        self.student_1._search_age(value=16, operator="in")
        # case:2 the method returns list of ids #T00475
        # loops through self.student_1._search_age(value=15, operator="in") twice and
        # using [0] gives output in a single list #T00475
        self.assertIn(
            self.student_1.id,
            [
                item
                for record in self.student_1._search_age(value=15, operator="in")[0]
                for item in record
            ],
        )
