from odoo import models


class StockMove(models.Model):
    _inherit = ["stock.move"]

    def _get_new_picking_values(self):
        """Inherited _get_new_picking_values() method to pass required field values from
        sale order to delivery order #T00382"""
        delivery_order_vals = super(StockMove, self)._get_new_picking_values()
        # for getting the sale order id and field value we use
        # group_id.sale_id.delivery_order_description and then pass value to DO #T00382
        delivery_order_vals[
            "delivery_order_description"
        ] = self.group_id.sale_id.delivery_order_description
        return delivery_order_vals

    def _prepare_procurement_values(self):
        """Inherited method to pass values from sale order to manufacturing order
        #T00396"""
        manufacture_order_vals = super(StockMove, self)._prepare_procurement_values()
        # for getting the sale order id and field value we use
        # group_id.sale_id.manufacturing_order_description and then pass value to
        # stock.move #T00396
        manufacture_order_vals[
            "manufacturing_order_description"
        ] = self.group_id.sale_id.manufacturing_order_description

        return manufacture_order_vals
