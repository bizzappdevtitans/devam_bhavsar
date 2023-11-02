from datetime import date

from dateutil.relativedelta import relativedelta

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestSchoolStudentFees(TransactionCase):
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
        self.payment_1 = self.env["school.student.fees"].create(
            {
                "name_student_id": self.student_1.id,
            }
        )

        super(TestSchoolStudentFees, self).setUp()

    def test_onchange_student_fees(self):
        """tests computed field compute_student_fees #T00475"""
        # case:1 where paid fees in set #T00475
        self.payment_1._onchange_student_fees()
        # case:2 where paid fees is set correctly #T00475
        self.payment_1.write({"paid_fees": 400})
        self.payment_1._onchange_student_fees()
        # case:3 where paid fees is set incorrectly #T00475
        with self.assertRaises(ValidationError):
            self.payment_1.write({"paid_fees": 40000})
            self.payment_1._onchange_student_fees()
