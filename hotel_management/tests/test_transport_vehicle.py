from odoo.tests.common import TransactionCase


class TestTransportVehicle(TransactionCase):
    def setUp(self):
        """Created a vehicle record to test #T00471"""
        self.vehicle_1 = self.env["transport.vehicle"].create(
            {
                "car_model": "test",
                "car_brand": "TEST",
                "car_type": "sedan",
            }
        )
        super(TestTransportVehicle, self).setUp()

    def test_name_get_vehicles(self):
        """Checks the name_get function is working properly or not #T00471"""
        res = self.vehicle_1.name_get()
        self.assertEqual(res[0][0], self.vehicle_1.id, "Fail")
