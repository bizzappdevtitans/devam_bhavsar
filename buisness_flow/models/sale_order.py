from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = ["sale.order"]

    # added field to pass values from SO to invoice #T00376
    invoice_description = fields.Text(string="Invoice description")
    # added field to pass values from SO to invoice #T00376
    delivery_description = fields.Text(string="Delivery description")
    # added field to pass values from SO to delivery order #T00382
    delivery_order_description = fields.Char(string="Delivery order description")
    # added field to pass values from SO to purchase order #T00387
    purchase_order_description = fields.Char(string="Purchase order description")
    # added field to pass values from SO to project #T00390
    project_requirements = fields.Char(string="Project requirements")
    # added field to pass values from SO to task #T00390
    task_requirements = fields.Char(string="Task requirements")
    # added field to pass values from SO to manufacturing order #T00396
    manufacturing_order_description = fields.Char(string="Manufacturing description")

    def _prepare_invoice(self):
        """Inherited _prepare_invoice method pass values from sale order to regular
        invoice #T00376"""
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        invoice_vals.update(
            {
                "invoice_description": self.invoice_description,
                "delivery_description": self.delivery_description,
            }
        )
        return invoice_vals
