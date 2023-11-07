from odoo import fields, models


class MrpProduction(models.Model):
    _inherit = ["mrp.production"]

    # added field in mrp.production by inherting it to store passed values from SO
    # T00396
    manufacturing_order_description = fields.Char(string="Manufacturing description")
