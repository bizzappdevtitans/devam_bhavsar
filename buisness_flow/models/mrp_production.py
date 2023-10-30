from odoo import fields, models


class MrpProduction(models.Model):
    _inherit = ["mrp.production"]

    manufacturing_order_description = fields.Char(string="Manufacturing description")
