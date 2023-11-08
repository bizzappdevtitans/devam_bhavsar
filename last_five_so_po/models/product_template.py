from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    # Added fields #T00447
    last_5_po_ids = fields.One2many(
        comodel_name="purchase.order",
        inverse_name="product_id",
        compute="_compute_last_five_po",
        string="Purchase orders",
    )

    last_5_so_ids = fields.One2many(
        comodel_name="sale.order",
        inverse_name="product_id",
        compute="_compute_last_five_so",
        string="Sale orders",
    )

    def _compute_last_five_po(self):
        """compute method to show last 5 po of a product #T00447"""
        for product in self:
            purchase_orders = self.env["purchase.order"].search(
                [
                    ("order_line.product_id", "in", product.product_variant_ids.ids),
                    ("state", "=", "purchase"),
                ],
                order="date_approve desc",
                limit=5,
            )
            self.write({"last_5_po_ids": purchase_orders})

    def _compute_last_five_so(self):
        """Compute method to show last 5 SO of a product #T00447"""
        for product in self:
            sale_orders = self.env["sale.order"].search(
                [
                    ("order_line.product_id", "in", product.product_variant_ids.ids),
                    ("state", "=", "sale"),
                ],
                order="date_order desc",
                limit=5,
            )
            self.write({"last_5_so_ids": sale_orders})
