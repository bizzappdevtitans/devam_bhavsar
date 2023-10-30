from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = ["sale.order"]

    invoice_description = fields.Text(string="Invoice description")
    delivery_description = fields.Text(string="Delivery description")
    delivery_order_description = fields.Char(string="Delivery order description")
    purchase_order_description = fields.Char(string="Purchase order description")
    project_requirements = fields.Char(string="Project requirements")
    task_requirements = fields.Char(string="Task requirements")
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
