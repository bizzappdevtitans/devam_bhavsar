from odoo.tests.common import TransactionCase


class TestRestaurantReservation(TransactionCase):
    def setUp(self):
        self.room_1 = self.env["hotel.room.type"].create(
            {
                "room_type": "single",
                "guests_ids": self.env.ref("base.res_partner_4"),
                "room_status": "booked",
            }
        )
        self.table_1 = self.env.create({"capacity": 2})
        self.guest_reservation_1 = self.env["restaurant.reservation"].create(
            {
                "guest_name_ids": self.room_1.guests_ids.ids,
                "room_no_id": self.room_1.id,
                "table_booking_list_ids": self.table_1.id,
            }
        )
        self.direct_reservation_1 = self.env["restaurant.reservation"].create(
            {
                "is_direct_reservation": True,
                "guest_name": "test1",
                "guest_email": "test1@test.com",
                "guest_phone": 9999999,
                "total_guests": 4,
            }
        )
        super(TestRestaurantReservation, self).setUp()
