from odoo import fields, models


class PurchaseOrder(models.Model):
    _inherit = ["purchase.order"]

    # added field in purchase.order by inherting it to store passed values from SO
    # T00387
    purchase_order_description = fields.Char(string="Purchase order description")
