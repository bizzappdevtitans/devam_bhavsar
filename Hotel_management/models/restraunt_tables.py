from odoo import _, api, fields, models


class RestrauntTable(models.Model):
    _name = "restraunt.tables"
    _description = "Restraunt Tables"
    _rec_name = "table_no_seq"

    table_no_seq = fields.Char("Table No", default=lambda self: _("New"))
    capacity = fields.Integer(string="Capacity")
    availability_status = fields.Selection(
        [("available", "Available"), ("reserved", "Reserved")], default="available"
    )

    @api.model
    def create(self, value):
        """Inherited create so at time of creation a unique sequence will be generated
        #T00471"""
        value["table_no_seq"] = self.env["ir.sequence"].next_by_code("restraunt.tables")
        return super(RestrauntTable, self).create(value)
