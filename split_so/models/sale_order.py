from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def prepare_split_vals(self):
        """Function to create child sale order #T00478"""
        categories = self.order_line.mapped("product_id.categ_id")
        for category in categories:
            orders = self.order_line.product_id.filtered(
                lambda x: x.categ_id == category
            )
            sale_order = self.create(
                {
                    "partner_id": self.partner_id.id,
                }
            )
            for product in orders.ids:
                self.env["sale.order.line"].create(
                    {
                        "order_id": sale_order.id,
                        "product_id": product,
                    }
                )
