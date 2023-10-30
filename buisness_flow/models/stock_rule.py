from odoo import models


class StockRule(models.Model):
    _inherit = "stock.rule"

    def _prepare_purchase_order(self, company_id, origins, values):
        """Inherited method to pass values from sale order to purchase order #T00387"""
        purchase_order_vals = super(StockRule, self)._prepare_purchase_order(
            company_id, origins, values
        )
        purchase_order_vals["purchase_order_description"] = (
            values[0].get("sale").purchase_order_description
        )
        return purchase_order_vals

    def _prepare_mo_vals(
        self,
        product_id,
        product_qty,
        product_uom,
        location_id,
        name,
        origin,
        company_id,
        values,
        bom,
    ):
        """Inherited method to pass values from sale order to manufacturing order
        #T00396"""
        manufacture_order_vals = super(StockRule, self)._prepare_mo_vals(
            product_id,
            product_qty,
            product_uom,
            location_id,
            name,
            origin,
            company_id,
            values,
            bom,
        )
        manufacture_order_vals["manufacturing_order_description"] = values.get(
            "manufacturing_order_description"
        )

        return manufacture_order_vals
