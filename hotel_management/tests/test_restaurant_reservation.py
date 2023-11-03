from datetime import date

from dateutil.relativedelta import relativedelta

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestRestaurantReservation(TransactionCase):
    def setUp(self):
        """created a room,table and two restaurant reservation one where
        is_direct_reservation is true and other where it isnt #T00471"""
        self.room_1 = self.env["hotel.room.type"].create(
            {
                "room_type": "single",
                "guests_ids": self.env.ref("base.res_partner_4"),
                "room_status": "booked",
            }
        )
        self.table_1 = self.env["restaurant.tables"].create({"capacity": 2})
        self.guest_reservation_1 = self.env["restaurant.reservation"].create(
            {
                "room_id": self.room_1.id,
                "table_booking_list_ids": self.table_1.ids,
                "reservation_date": date.today() + relativedelta(days=1),
            }
        )
        self.direct_reservation_1 = self.env["restaurant.reservation"].create(
            {
                "guest_email": "test1@test.com",
                "guest_phone": 9999999,
                "total_guests": 4,
                "reservation_date": date.today() + relativedelta(days=1),
            }
        )
        super(TestRestaurantReservation, self).setUp()

    def test_onchange_get_guests_from_room(self):
        """checks if the onchange methods works properly #T00475"""
        self.guest_reservation_1._onchange_get_guests_from_room()
        self.assertEqual(
            self.guest_reservation_1.guest_ids.ids,
            self.room_1.guests_ids.ids,
        )

    def test_action_confirm(self):
        """Checks if action confirm works properly by checking if tables status has
        changed or not #T00471"""
        self.guest_reservation_1._onchange_get_guests_from_room()
        self.guest_reservation_1.action_confirm()
        self.assertEqual(
            self.guest_reservation_1.table_booking_list_ids.availability_status,
            "reserved",
            "Fail",
        )

    def test_action_cancel(self):
        """Checks if action cancel works properly by checking if tables status has
        changed or not #T00471"""
        self.guest_reservation_1.action_cancel()
        self.assertEqual(
            self.guest_reservation_1.table_booking_list_ids.availability_status,
            "available",
            "Fail",
        )

    def test_action_cancel_to_draft(self):
        """Checks if action cancel_to_draft works properly by checking if reservation
        status has changed or not #T00471"""
        self.guest_reservation_1.action_cancel_to_draft()
        self.assertEqual(
            self.guest_reservation_1.restaurant_reservation_states, "draft", "Fail"
        )

    def test_reservation_date(self):
        """Checks if validation error is raised if wrong date input is set #T00471"""
        with self.assertRaises(ValidationError):
            self.direct_reservation_1.write(
                {"reservation_date": date.today() - relativedelta(days=1)}
            )
