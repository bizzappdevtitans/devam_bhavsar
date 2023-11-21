from odoo.tests.common import TransactionCase


class TestSaleOrderLine(TransactionCase):
    def setUp(self):
        """Created a sale order with order_lines #T00485"""
        super(TestSaleOrderLine, self).setUp()
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

    def test_onchange_product_vendor(self):
        """Checks if the _onchange_product_vendor works properly #T00485"""
        self.sale_order_1.order_line._onchange_product_vendor()
        # Checks if the vendor_id lies in product's seller_ids
        self.assertIn(
            self.sale_order_1.order_line.vendor_id,
            self.sale_order_1.order_line.product_id.seller_ids,
            "Product vendor isn't in seller_ids",
        )
        # Change product_id to a product that doesn't have any vendors
        self.sale_order_1.order_line.write(
            {"product_id": self.env.ref("product.product_product_3").id}
        )
        self.sale_order_1.order_line._onchange_product_vendor()
        # Checks if the vendor_id is false for the product with no vendors
        self.assertFalse(
            self.sale_order_1.order_line.vendor_id,
            "Vendor_id of product with no vendors is not False",
        )
