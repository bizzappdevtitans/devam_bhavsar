from odoo import _, fields, models
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    # Added field #T00478
    parent_sale_order_id = fields.Many2one(
        comodel_name="sale.order", string="Parent sale order"
    )
    child_so_count = fields.Integer(
        string="Child SO", compute="_compute_child_so_count"
    )

    def _compute_child_so_count(self):
        """Compute method to calculate number of child sale orders made #T00478"""
        for count_of_child_so in self:
            count_of_child_so.child_so_count = self.env["sale.order"].search_count(
                [("parent_sale_order_id", "=", count_of_child_so.id)]
            )

    def split_so_by_category(self):
        """Function to create sale order for each category products #T00478"""
        lines = self.mapped("order_line")
        categories = lines.mapped("product_id.categ_id")
        if len(categories) <= 1:
            raise ValidationError(
                _(f"Can't split,only one category {lines.product_id.categ_id.name}")
            )
        for category in categories:
            orders = lines.filtered(
                lambda product: product.product_id.categ_id == category
            )
            new_lines = []
            for products in orders:
                new_lines.append(
                    (
                        0,
                        0,
                        {
                            "product_id": products.product_id.id,
                            "product_uom_qty": products.product_uom_qty,
                        },
                    )
                )
            self.create(
                {
                    "parent_sale_order_id": self.id,
                    "partner_id": self.partner_id.id,
                    "order_line": new_lines,
                }
            )

    def split_so_per_line(self):
        """Function to create sale orders for each order_line #T00478"""
        lines = self.mapped("order_line")
        if len(lines) <= 1:
            raise ValidationError(
                _(f"Can't split,there's only one product {lines.product_id.name}")
            )
        for products in lines:
            sale_order = self.create(
                {
                    "parent_sale_order_id": self.id,
                    "partner_id": self.partner_id.id,
                }
            )
            self.env["sale.order.line"].create(
                {
                    "order_id": sale_order.id,
                    "product_id": products.product_id.id,
                    "product_uom_qty": products.product_uom_qty,
                }
            )

    def action_show_child_so(self):
        """action of smart button to show child sale orders #T00478"""
        return {
            "type": "ir.actions.act_window",
            "name": "Sale orders",
            "view_mode": "tree,form",
            "res_model": "sale.order",
            "domain": [("parent_sale_order_id", "=", self.id)],
            "target": "current",
        }
