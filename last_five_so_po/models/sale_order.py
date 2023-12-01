from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    # Added fields #T00447
    product_id = fields.Many2one(
        "product.product", string="Product", related="order_line.product_id"
    )
