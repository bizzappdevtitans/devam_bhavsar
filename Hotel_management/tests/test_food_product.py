from odoo.tests.common import TransactionCase


class TestFoodProduct(TransactionCase):
    def setUp(self):
        self.food_item_1 = self.env["food.product"].create(
            {
                "food_name": "test",
                "food_price": "20",
                "food_calory": "50",
                "food_qty": 5,
            }
        )
        super(TestFoodProduct, self).setUp()

    def test_subtotal(self):
        """Checks if the computed method gives intended value #T00471"""
        self.assertEqual(self.food_item_1.food_subtotal, 100, "Fail")
