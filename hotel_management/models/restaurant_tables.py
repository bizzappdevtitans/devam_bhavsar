from odoo import _, api, fields, models


class RestaurantTable(models.Model):
    _name = "restaurant.tables"
    _description = "restaurant Tables"
    _rec_name = "table_no_seq"

    # Added required fields #T00471
    table_no_seq = fields.Char("Table No", default=lambda self: _("New"))
    capacity = fields.Integer(string="Capacity")
    availability_status = fields.Selection(
        [("available", "Available"), ("reserved", "Reserved")], default="available"
    )
    restaurant_reservation_ref = fields.Many2one(
        comodel_name="restaurant.reservation", string="Reservation no."
    )

    @api.model
    def create(self, value):
        """Inherited create so at time of creation a unique sequence will be generated
        #T00471"""
        value["table_no_seq"] = self.env["ir.sequence"].next_by_code(
            "restaurant.tables"
        )
        return super(RestaurantTable, self).create(value)
