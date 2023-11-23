from datetime import date

from dateutil.relativedelta import relativedelta

from odoo.tests.common import TransactionCase


class TestSchoolTeacherLeave(TransactionCase):
    def setUp(self):
        """created a teacher and teacher leave record #T00475"""
        super(TestSchoolTeacherLeave, self).setUp()
        self.teacher_1 = self.env["school.teacher"].create(
            {
                "first_name": "test_first_name",
                "last_name": "test_last_name",
                "date_of_birth": date.today() - relativedelta(years=25),
            }
        )
        self.teacher_leave_1 = self.env["school.teacher.leave"].create(
            {
                "teacher_name_id": self.teacher_1.id,
                "leave_date_from": date.today() + relativedelta(days=1),
                "leave_date_to": date.today() + relativedelta(days=4),
            }
        )

    def test_compute_total_days(self):
        """tests the computed field compute_total_days #T00475"""
        self.assertEqual(self.teacher_leave_1.total_days, 3, "Total days dosent match")

    def test_inverse_calculate_date_from_total_days(self):
        """tests inverse_calculate_date_from_total_days method #T00475"""
        self.teacher_leave_1.write({"total_days": 10})
        self.assertEqual(
            self.teacher_leave_1.leave_date_to,
            self.teacher_leave_1.leave_date_from
            + relativedelta(days=self.teacher_leave_1.total_days),
            "leave date to dosent match",
        )
