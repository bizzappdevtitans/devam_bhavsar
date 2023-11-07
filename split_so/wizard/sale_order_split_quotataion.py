from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SaleOrderSplitQuotation(models.TransientModel):
    _name = "sale.order.split.quotation"
    _description = "Split sale orders"

    # Added fields #T00478
    is_split_so_based_on_category = fields.Boolean(string="Split based on category")
    sale_order_id = fields.Many2one(
        comodel_name="sale.order",
        string="Sale order",
        default=lambda self: self._default_sale_order(),
    )

    def action_confirm(self):
        """confirm action of wizard #T00478"""
        if not self.is_split_so_based_on_category:
            raise ValidationError(_("Please select a criteria to split sale orders on"))
        self.sale_order_id.create_split_so()

    @api.model
    def _default_sale_order(self):
        """function to get default name of teacher in wizard #T00478"""
        context = dict(self._context) or {}
        sale_order = self.env["sale.order"].browse(context.get("active_id", False))
        return sale_order and sale_order.id
