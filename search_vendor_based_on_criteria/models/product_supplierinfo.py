from odoo import fields, models


class ProductSupplierInfo(models.Model):
    _inherit = "product.supplierinfo"

    supplier_sequence = fields.Integer(string="Priority sequence")
