from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SaleOrderSplitQuotation(models.TransientModel):
    _name = "sale.order.split.quotation"
    _description = "Split sale orders"

    # Added fields #T00478
    split_so_options = fields.Selection(
        [
            ("category", "Category"),
            ("selected_lines", "Selected lines"),
            ("one_line_per_order", "One line per order"),
        ],
        required=True,
    )
    sale_order_id = fields.Many2one(
        comodel_name="sale.order",
        string="Sale order",
        default=lambda self: self._default_sale_order(),
    )
    sale_order_line_ids = fields.Many2many(
        comodel_name="sale.order.line",
        relation="sale_order_and_order_line_rel",
        column1="sale_order_line_ids",
        column2="order_id",
        string="Sale order lines",
        domain=lambda self: [("id", "in", self.get_order_lines().ids)],
    )

    @api.model
    def _default_sale_order(self):
        """function to get default name of teacher in wizard #T00478"""
        context = dict(self._context) or {}
        sale_order = self.env["sale.order"].browse(context.get("active_id", False))
        return sale_order

    def get_order_lines(self):
        """Function to get order_lines from current sale order #T00478"""
        sale_orders = self._default_sale_order()
        order_lines = sale_orders.mapped("order_line")
        return order_lines

    def split_so_by_selected_line(self):
        """Function that creates a sale order from selected lines #T00478"""
        if not self.sale_order_line_ids:
            raise ValidationError(_("Please select products"))
        for lines in self.sale_order_line_ids:
            new_lines = []
            for product in lines:
                new_lines.append(
                    (
                        0,
                        0,
                        {
                            "product_id": product.product_id.id,
                            "product_uom_qty": product.product_uom_qty,
                        },
                    )
                )
            self.env["sale.order"].create(
                {
                    "parent_sale_order_id": self.sale_order_id.id,
                    "partner_id": self.sale_order_id.partner_id.id,
                    "order_line": new_lines,
                }
            )

    def action_confirm(self):
        """confirm action of wizard #T00478"""
        if self.split_so_options == "category":
            self.sale_order_id.split_so_by_category()
        if self.split_so_options == "selected_lines":
            self.split_so_by_selected_line()
        if self.split_so_options == "one_line_per_order":
            self.sale_order_id.split_so_per_line()
