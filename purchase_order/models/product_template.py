from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    last_5_po = fields.One2many(
        comodel_name="purchase.order",
        inverse_name="product_id",
        compute="_compute_last_5_po",
        string="Purchase order",
    )

    def _compute_last_5_po(self):
        """compute method to show last 5 po of a product #T00447"""
        for product in self:
            purchase_orders = self.env["purchase.order"].search(
                [
                    "&",
                    ("order_line.product_id.id", "in", product.product_variant_ids.ids),
                    ("state", "=", "purchase"),
                ],
                order="date_approve desc",
                limit=5,
            )
        self.last_5_po = purchase_orders
