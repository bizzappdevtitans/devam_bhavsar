from odoo.tests.common import TransactionCase


class TestSaleOrder(TransactionCase):
    def setUp(self):
        """Created sale order with order_lines,products with product categories and
        wizard #T00478"""
        super(TestSaleOrder, self).setUp()
        self.product_1 = self.env["product.product"].create({"name": "Test Product 1"})
        self.product_2 = self.env["product.product"].create({"name": "Test Product 2"})
        self.sale_order_1 = self.env["sale.order"].create(
            {
                "partner_id": self.env.ref("base.res_partner_4").id,
                "order_line": [
                    (0, 0, {"product_id": self.product_1.id, "product_uom_qty": 10}),
                    (0, 0, {"product_id": self.product_2.id, "product_uom_qty": 50}),
                ],
            }
        )
        self.wizard_1 = (
            self.env["sale.order.split.quotation"]
            .with_context(active_id=self.sale_order_1.id)
            .create({"split_so_options": "one_line_per_order"})
        )

    def test_compute_child_so_count(self):
        """Checks if the compute method is working properly #T00478"""
        self.wizard_1.action_confirm()
        self.assertEqual(
            self.sale_order_1.child_so_count, 2, "Child so count is incorect"
        )

    def test_action_show_child_so(self):
        """Checks if the smart button is working properly #T00478"""
        domain = [("parent_sale_order_id", "=", self.sale_order_1.id)]
        self.assertListEqual(
            domain,
            self.sale_order_1.action_show_child_so().get("domain"),
            "Smart button isn't working properly",
        )
