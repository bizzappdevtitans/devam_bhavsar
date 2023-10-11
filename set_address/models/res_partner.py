from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    is_delivery_address = fields.Boolean(string="Set Delivery address")
    type = fields.Selection(selection_add=[("dropship", "Drop shiping Address")])
