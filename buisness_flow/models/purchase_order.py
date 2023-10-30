from odoo import fields, models


class PurchaseOrder(models.Model):
    _inherit = ["purchase.order"]

    purchase_order_description = fields.Char(string="Purchase order description")
