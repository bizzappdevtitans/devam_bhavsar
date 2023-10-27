from datetime import date

from dateutil.relativedelta import relativedelta

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestHotelRoomReservation(TransactionCase):
    def setUp(self):
        """Create three records of rooms with each room types and 3 records for
        each room type accordingly #T00471"""
        self.room_single = self.env["hotel.room.type"].create({"room_type": "single"})
        self.room_double = self.env["hotel.room.type"].create({"room_type": "double"})
        self.room_family = self.env["hotel.room.type"].create({"room_type": "family"})
        self.room_reservation_single = self.env["hotel.room.reservation"].create(
            {
                "customer_ids": self.env.ref("base.res_partner_4"),
                "rooms_ids": self.room_single.ids,
                "check_in_date": date.today() + relativedelta(days=1),
                "check_out_date": date.today() + relativedelta(days=3),
            }
        )
        partner = self.env["res.partner"].search([], limit=3)
        self.room_reservation_double = self.env["hotel.room.reservation"].create(
            {
                "customer_ids": partner,
                "rooms_ids": self.room_double.ids,
                "check_in_date": date.today() + relativedelta(days=1),
                "check_out_date": date.today() + relativedelta(days=2),
            }
        )
        self.room_reservation_family = self.env["hotel.room.reservation"].create(
            {
                "customer_ids": self.env.ref("base.res_partner_4"),
                "rooms_ids": self.room_family.ids,
                "check_in_date": date.today() + relativedelta(days=1),
                "check_out_date": date.today() + relativedelta(days=2),
            }
        )

        super(TestHotelRoomReservation, self).setUp()

    def test_room_reservation_single(self):
        """Function that for testing single type room reservation #T00471"""
        # confirms the reservation by calling the confirm button #T00471
        self.room_reservation_single.action_confirm()
        # checks if the rooms reservation_ref field id is same as reservation id
        # as intended #T00471
        self.assertEqual(
            self.room_single.reservation_ref.id,
            self.room_reservation_single.id,
            "success",
        )
        # checks if the computed field total_cost has intended value #T00471
        self.assertEqual(self.room_reservation_single.total_cost, 2020.0, "Fail")
        self.room_reservation_single.action_cancel()
        self.room_reservation_single.action_cancel_to_draft()
        reservations = (
            self.env["hotel.room.reservation"]
            .search([])
            .filtered(
                lambda dates: dates.reservation_status == "reserved"
                and (dates.check_in_date - relativedelta(weeks=1)) == date.today()
            )
        )
        # checks if the records are searched for cron job are correct #T00471
        self.assertEqual(
            self.room_reservation_single.get_reservation(),
            reservations,
            "Fail",
        )

    def test_room_reservation_double(self):
        """Function that for testing double type room reservation #T00471"""
        # checks room_capacity constrain #T00471
        with self.assertRaises(ValidationError):
            self.room_reservation_double.action_confirm()

    def test_room_reservation_family(self):
        """Function that for testing family type room reservation #T00471"""
        # checks if check in date is proper or not #T00471
        with self.assertRaises(ValidationError):
            self.room_reservation_family.write(
                {"check_in_date": date.today() - relativedelta(days=2)}
            )
        # checks if check in date  and check out date is proper or not #T00471
        with self.assertRaises(ValidationError):
            self.room_reservation_family.write(
                {
                    "check_in_date": date.today() + relativedelta(days=2),
                    "check_out_date": date.today(),
                }
            )
