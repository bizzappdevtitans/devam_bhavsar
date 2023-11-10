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
        """Function to create child sale order #T00478"""
        lines = self.mapped("order_line")
        categories = lines.mapped("product_id.categ_id")
        sale_lines = {}
        if len(categories) <= 1:
            raise ValidationError(_("Cant split, theres only one categories products"))
        for category in categories:
            orders = lines.product_id.filtered(
                lambda product: product.categ_id == category
            )
            for products in orders.ids:
                sale_lines["products"] = products
            for qty in lines:
                sale_lines["qty"] = qty.product_uom_qty
        sale_order = self.create(
            {
                "parent_sale_order_id": self.id,
                "partner_id": self.partner_id.id,
            }
        )

        self.env["sale.order.line"].create(
            {
                "order_id": sale_order.id,
                "product_id": products,
                "product_uom_qty": qty,
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
