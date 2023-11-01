from datetime import date

from dateutil.relativedelta import relativedelta

from odoo.tests.common import TransactionCase


class TestSchoolPrincipl(TransactionCase):
    def setUp(self):
        self.principal_1 = self.env["school.principal"].create(
            {
                "principal_first_name": "TEST",
                "principal_last_name": "test",
                "date_of_birth": date.today() - relativedelta(years=69),
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
            }
        )
        super(TestSchoolPrincipl, self).setUp()

    def test_compute_principal_age(self):
        """tests computed field age_principal #T00475"""
        self.assertEqual(self.principal_1.age_principal, 69, "Fail")

    def test_action_change_state_to_confirm_info(self):
        """tests action_change_state_to_confirm_info method #T00475"""
        self.student_1.write({"is_confirm_info": True})
        # search  all students record that fits the criteria #T00475
        students = self.env["school.student"].search([("is_confirm_info", "=", True)])
        self.principal_1.action_change_state_to_confirm_info()
        # checks if the searched records states has changed #T00475
        self.assertEqual(students.admission_state, "confirm_info", "Fail")

    def test_action_change_state_to_confirm_admission(self):
        """tests action_change_state_to_confirm_info method #T00475"""
        self.student_1.write({"is_confirm_admission": True})
        # search  all students record that fits the criteria #T00475
        students = self.env["school.student"].search(
            [("is_confirm_admission", "=", True)]
        )
        self.principal_1.action_change_state_to_confirm_admission()
        # checks if the searched records states has changed #T00475
        self.assertEqual(students.admission_state, "admitted", "Fail")
