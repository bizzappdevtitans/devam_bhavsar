from odoo.tests.common import TransactionCase


class TestProductSupplierinfo(TransactionCase):
    def setUp(self):
        """Created a new supplier record #T00485"""
        super(TestProductSupplierinfo, self).setUp()
        self.supplier_1 = self.env["product.supplierinfo"].create(
            {
                "name": self.env.ref("base.res_partner_4").id,
                "product_tmpl_id": self.env.ref(
                    "product.product_delivery_01"
                ).product_tmpl_id.id,
                "delay": 7,
                "price": 100,
            }
        )

    def test_name_get(self):
        """Checks if the name_get works properly #T00485"""
        res = self.supplier_1.name_get()
        self.assertEqual(
            res[0][0], self.supplier_1.id, "name_get doesn't work properly"
        )
