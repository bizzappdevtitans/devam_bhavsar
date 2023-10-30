from odoo import models


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    def _prepare_invoice_values(self, order, name, amount, so_line):
        """Inherited method for passing value from sale order to
        downpayment invoice.#T00376"""
        invoice_vals = super(SaleAdvancePaymentInv, self)._prepare_invoice_values(
            order, name, amount, so_line
        )
        invoice_vals.update(
            {
                "invoice_description": order.invoice_description,
                "delivery_description": order.delivery_description,
            }
        )
        return invoice_vals
