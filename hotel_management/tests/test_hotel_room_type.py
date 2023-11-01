from datetime import date

from dateutil.relativedelta import relativedelta

from odoo.tests.common import TransactionCase


class TestHotelRoomType(TransactionCase):
    def setUp(self):
        """Create four records of rooms with each room types #T00471"""

        self.room_single = self.env["hotel.room.type"].create(
            {
                "room_type": "single",
                "guests_ids": self.env.ref("base.res_partner_4"),
                "room_status": "booked",
            }
        )
        self.room_double = self.env["hotel.room.type"].create({"room_type": "double"})
        self.room_family = self.env["hotel.room.type"].create({"room_type": "family"})
        self.room_vip = self.env["hotel.room.type"].create({"room_type": "vip"})
        self.room_reservation_1 = self.env["hotel.room.reservation"].create(
            {
                "customer_ids": self.env.ref("base.res_partner_4"),
                "rooms_ids": self.room_single.ids,
                "check_in_date": date.today() + relativedelta(weeks=1),
                "check_out_date": date.today() + relativedelta(days=13),
            }
        )
        super(TestHotelRoomType, self).setUp()

    def test_room_capacity(self):
        """Checks if room capacity is proper or not #T00471"""
        self.assertEqual(self.room_family.room_capacity, 4, "Fail")
        self.assertEqual(self.room_vip.room_capacity, 2, "Fail")

    def test_room_price(self):
        """Checks room price #T00471"""
        self.assertEqual(self.room_double.room_price, 2020.0, "Fail")
        self.assertEqual(self.room_family.room_price, 3030.0, "Fail")
        self.assertEqual(self.room_vip.room_price, 4040.0, "Fail")

    def test_name_get(self):
        """Checks the name_get function is proper or not #T00471"""
        res = self.room_double.name_get()
        self.assertEqual(res[0][0], self.room_double.id, "Fail")

    def test_guest_count(self):
        """Checks if the computed field guest counts value is as proper or not #T00471"""
        self.assertEqual(
            len(self.room_single.guests_ids), self.room_single.guests_count, "Fail"
        )

    def test_action_show_guests(self):
        """Function to check action of smart button #T00471"""
        self.room_single.action_show_guests()

    def test_action_checkout(self):
        """Checks if the checkout button works as intended #T00471"""
        self.room_reservation_1.action_confirm()
        self.room_single.action_checkout()
        self.assertEqual(
            self.room_single.reservation_ref.reservation_status, "done", "fail"
        )
