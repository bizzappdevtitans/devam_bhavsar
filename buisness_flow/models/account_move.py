from odoo import fields, models


class AccountMove(models.Model):
    _inherit = ["account.move"]

    invoice_description = fields.Text(string="Invoice description")
    delivery_description = fields.Text(string="Delivery description")
