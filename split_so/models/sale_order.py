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

    def create_split_so(self):
        """Function to create child sale order #T00478"""
        categories = self.order_line.mapped("product_id.categ_id")
        if len(categories) <= 1:
            raise ValidationError(_("Cant split, theres only one categories products"))
        for category in categories:
            orders = self.order_line.product_id.filtered(
                lambda product: product.categ_id == category
            )
            sale_order = self.create(
                {
                    "parent_sale_order_id": self.id,
                    "partner_id": self.partner_id.id,
                }
            )
            for products in orders.ids:
                self.env["sale.order.line"].create(
                    {
                        "order_id": sale_order.id,
                        "product_id": products,
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
