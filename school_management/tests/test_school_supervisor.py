from datetime import date

from dateutil.relativedelta import relativedelta

from odoo.tests.common import TransactionCase


class TestSchoolSupervisor(TransactionCase):
    def setUp(self):
        """Created a teacher and supervisor record #T00475"""
        super(TestSchoolSupervisor, self).setUp()
        self.teacher_1 = self.env["school.teacher"].create(
            {
                "first_name": "test_first_name",
                "last_name": "test_last_name",
                "date_of_birth": date.today() - relativedelta(years=25),
            }
        )
        self.supervisor_1 = self.env["school.supervisor"].create(
            {
                "supervisor_first_name": "TEST",
                "supervisor_last_name": "test",
                "date_of_birth": date.today() - relativedelta(years=55),
                "assigned_teachers_of_supervisor_ids": self.teacher_1,
                "email_supervisor": "test@gmail.com",
            }
        )

    def test_compute_age(self):
        """tests computed field age_supervisor #T00475"""
        self.assertEqual(
            self.supervisor_1.age_supervisor, 55, "Supervisor age dosent match"
        )

    def test_name_get(self):
        """tests name_get function #T00475"""
        res = self.supervisor_1.name_get()
        self.assertEqual(
            res[0][0], self.supervisor_1.id, "name_get function dosent work"
        )
