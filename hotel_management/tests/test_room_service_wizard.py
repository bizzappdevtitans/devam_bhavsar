from datetime import datetime

from odoo.tests.common import TransactionCase


class TestRoomServiceWizard(TransactionCase):
    def setUp(self):
        """Created a vehicle,food,room and two hotel.room.service.record each for
        each type to test all methods #T00471"""
        self.vehicle_1 = self.env["transport.vehicle"].create(
            {
                "car_model": "test",
                "car_brand": "TEST",
                "car_type": "sedan",
            }
        )
        self.food_item_1 = self.env["food.product"].create(
            {
                "food_name": "test",
                "food_price": "20",
                "food_calory": "50",
                "food_qty": 5,
            }
        )
        self.room_1 = self.env["hotel.room.type"].create(
            {
                "room_type": "single",
                "guests_ids": self.env.ref("base.res_partner_4"),
                "room_status": "booked",
            }
        )
        self.service_transport = self.env["hotel.room.service.wizard"].create(
            {
                "service_type": "transport",
                "room_id": self.room_1.id,
                "pick_up_location": "Test",
                "pick_up_datetime": datetime.now(),
                "destination_location": "TEST",
                "car_lines_ids": self.vehicle_1.ids,
            }
        )
        self.service_food = self.env["hotel.room.service.wizard"].create(
            {
                "service_type": "food",
                "room_id": self.room_1.id,
                "food_lines_ids": self.food_item_1.ids,
            }
        )

        super(TestRoomServiceWizard, self).setUp()

    def test_action_order_service(self):
        """Function to test action order service method #T00471"""
        self.service_transport._default_room_number()
        self.service_food.action_order_service()
        self.service_transport.action_order_service()
