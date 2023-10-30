from odoo import fields, models


class AccountMove(models.Model):
    _inherit = ["account.move"]

    # added field in account.move by inherting it to store passed values from SO #T00376
    invoice_description = fields.Text(string="Invoice description")
    delivery_description = fields.Text(string="Delivery description")
