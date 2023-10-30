from odoo import fields, models


class StockPicking(models.Model):
    _inherit = ["stock.picking"]

    delivery_order_description = fields.Char(string="Delivery order description")
