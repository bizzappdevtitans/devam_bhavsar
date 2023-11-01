from datetime import date

from dateutil.relativedelta import relativedelta

from odoo.tests.common import TransactionCase


class TestSchoolStudentFees(TransactionCase):
    def setUp(self):
        """Created a pyment and student record #T00475"""
        self.payment_1 = self.env["school.student.fees"].create(
            {"paid_fees": 200, "total_fees": 500}
        )
        self.student_1 = self.env["school.student"].create(
            {
                "student_first_name": "Test1",
                "student_last_name": "Test1",
                "rollno": 1,
                "date_of_birth": date.today() - relativedelta(years=15),
                "address_student": "TEST",
                "standard": "standard1",
                "fees_students_ids": [
                    (6, 0, [self.payment_1.id]),
                ],
            }
        )

        super(TestSchoolStudentFees, self).setUp()

    def test_compute_student_fees(self):
        """tests computed field compute_student_fees #T00475"""
        self.payment_1.write({"paid_fees": 40000})
