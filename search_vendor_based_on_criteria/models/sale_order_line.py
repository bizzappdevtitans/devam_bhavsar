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
        """Onchange function to get vendors based on criteria:
        1.The vendor with lowest price will be selected
        2.If multiple vendors of same product has minimum or same price, then
        the vendor with  minimum delivery lead time will be selected
        3.If both price and delivery lead time is same then the vendor with the lowest
        vendor_sequence will be selected #T00485"""
        for product in self:
            if not product.product_id.seller_ids:
                product.vendor_id = False
            vendors = self.env["product.supplierinfo"].search(
                [("id", "in", self.product_id.seller_ids.ids)],
                order="price asc , delay asc, vendor_sequence asc",
                limit=1,
            )
            product.vendor_id = vendors
