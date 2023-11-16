from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    # Added field #T00485
    vendor_id = fields.Many2one(
        comodel_name="product.supplierinfo",
        string="Vendor",
    )

    @api.onchange("product_id")
    def _onchange_product_vendor(self):
        """Onchange function to get vendors based on criterias #T00485"""
        if self.product_id:
            vendors = self.env["product.supplierinfo"].search(
                [("product_id", "=", self.product_id.id)]
            )
            sort_vendor_by_price = vendors.sorted(key=lambda product: product.price)
            self.vendor_id = sort_vendor_by_price[0]
