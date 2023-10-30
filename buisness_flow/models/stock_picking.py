from odoo import fields, models


class StockPicking(models.Model):
    _inherit = ["stock.picking"]

    # added field in stock.picking by inherting it to store passed values from SO
    # T00382
    delivery_order_description = fields.Char(string="Delivery order description")
