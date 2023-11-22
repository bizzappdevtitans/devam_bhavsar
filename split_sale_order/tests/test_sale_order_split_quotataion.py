from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestSaleOrderSplitQuotation(TransactionCase):
    def setUp(self):
        """Created sale order with order_lines,products with product categories and
        wizard for each split option #T00478"""
        super(TestSaleOrderSplitQuotation, self).setUp()
        self.sale_order_1 = self.env["sale.order"].create(
            {
                "partner_id": self.env.ref("base.res_partner_4").id,
                "order_line": [
                    (
                        0,
                        0,
                        {"product_id": self.env.ref("product.product_delivery_01").id},
                    )
                ],
            }
        )

        self.category_1 = self.env["product.category"].create(
            {"name": "Test Category 1"}
        )
        self.category_2 = self.env["product.category"].create(
            {"name": "Test Category 2"}
        )
        self.product_1 = self.env["product.product"].create(
            {"name": "Test Product 1", "categ_id": self.category_1.id}
        )
        self.product_2 = self.env["product.product"].create(
            {"name": "Test Product 2", "categ_id": self.category_2.id}
        )
        self.sale_order_1 = self.env["sale.order"].create(
            {
                "partner_id": self.env.ref("base.res_partner_4").id,
                "order_line": [
                    (0, 0, {"product_id": self.product_1.id, "product_uom_qty": 50})
                ],
            }
        )

        self.wizard_1 = (
            self.env["sale.order.split.quotation"]
            .with_context(active_id=self.sale_order_1.id)
            .create({"split_so_options": "category"})
        )
        self.wizard_2 = (
            self.env["sale.order.split.quotation"]
            .with_context(active_id=self.sale_order_1.id)
            .create({"split_so_options": "selected_lines"})
        )
        self.wizard_3 = (
            self.env["sale.order.split.quotation"]
            .with_context(active_id=self.sale_order_1.id)
            .create({"split_so_options": "one_line_per_order"})
        )

    def test_split_so_by_category(self):
        """Checks if sale orders are being split by category properly #T00478"""
        # Checks for validation error when there's only one category product #T00478
        with self.assertRaises(ValidationError):
            self.wizard_1.action_confirm()
        # Adds a different category product #T00478
        self.sale_order_1.write(
            {
                "order_line": [
                    (0, 0, {"product_id": self.product_2.id, "product_uom_qty": 30})
                ]
            }
        )
        self.wizard_1.action_confirm()
        child_orders = self.env["sale.order"].search(
            [("parent_sale_order_id", "=", self.sale_order_1.id)]
        )
        self.assertEqual(len(child_orders), 2, "Split by category is not working")

    def test_split_so_by_selected_line(self):
        """Checks if sale orders are being split by selected order lines
        properly #T00478"""
        # checks for validation error when user didn't select any product #T00478
        with self.assertRaises(ValidationError):
            self.wizard_2.action_confirm()
        # Add a second product #T00478
        self.sale_order_1.write(
            {
                "order_line": [
                    (0, 0, {"product_id": self.product_2.id, "product_uom_qty": 30})
                ]
            }
        )
        # Add the order_line that needs to be split #T00478
        self.wizard_2.write(
            {
                "sale_order_line_ids": [
                    (
                        0,
                        0,
                        {
                            "order_id": self.sale_order_1.id,
                            "product_id": self.product_1.id,
                            "product_uom_qty": 50,
                        },
                    ),
                ],
            }
        )

        self.wizard_2.action_confirm()
        child_orders = self.env["sale.order"].search(
            [("parent_sale_order_id", "=", self.sale_order_1.id)]
        )
        self.assertEqual(len(child_orders), 1, "Split by selected lines is not working")

    def test_split_so_per_line(self):
        """Checks if sale orders are being split per order line properly #T00478"""
        # checks for validation error when there's no product in order_line #T00478
        with self.assertRaises(ValidationError):
            self.wizard_3.action_confirm()
        # Add a product in order_line #T00478
        self.sale_order_1.write(
            {
                "order_line": [
                    (0, 0, {"product_id": self.product_2.id, "product_uom_qty": 30})
                ]
            }
        )
        self.wizard_3.action_confirm()
        child_orders = self.env["sale.order"].search(
            [("parent_sale_order_id", "=", self.sale_order_1.id)]
        )
        self.assertEqual(len(child_orders), 2, "Split per lines is not working")
