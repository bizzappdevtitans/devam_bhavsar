from odoo import _, api, fields, models


class HotelRoomServices(models.Model):
    _name = "hotel.room.services"
    _description = "Hotel room services"
    _rec_name = "service_order_number_seq"

    service_type = fields.Selection(
        [("food", "Food service"), ("room_keeping", "Room Keeping service")]
    )
    room_id = fields.Many2one(comodel_name="hotel.room.type", string="Room number")
    food_lines_ids = fields.One2many(
        comodel_name="hotel.room.service.food.line",
        inverse_name="food_service_id",
        string="Food",
    )
    service_order_number_seq = fields.Char(
        string="Service order number", default=lambda self: _("New")
    )

    @api.model
    def create(self, value):
        """Inherited create so at time of creation a unique sequence will be generated
        #T00471"""
        value["service_order_number_seq"] = self.env["ir.sequence"].next_by_code(
            "hotel.room.services"
        )
        return super(HotelRoomServices, self).create(value)
