from odoo import api, fields, models


class ProductSupplierInfo(models.Model):
    _inherit = "product.supplierinfo"

    # Added field #T00485
    vendor_sequence = fields.Integer(string="Vendor sequence")
    _sql_constraints = [
        (
            "unique_vendor_sequence",
            "UNIQUE(product_tmpl_id,vendor_sequence)",
            "This sequence is already assigned to a vendor",
        ),
    ]

    @api.model
    def name_get(self):
        """overided name_get so that vendor name and price is shown #T00485"""
        result = []
        for combined_name in self:
            result.append(
                (
                    combined_name.id,
                    "%s [%s%s]"
                    % (
                        combined_name.name.name,
                        combined_name.currency_id.symbol,
                        combined_name.price,
                    ),
                )
            )
        return result
