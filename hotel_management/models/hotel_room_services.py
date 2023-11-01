from odoo import _, api, fields, models


class HotelRoomServices(models.Model):
    _name = "hotel.room.services"
    _description = "Hotel room services"
    _rec_name = "service_order_number_seq"

    # Added required fields #T00471
    service_type = fields.Selection(
        [("food", "Food service"), ("transport", "Transportation service")],
        required=True,
    )
    service_order_number_seq = fields.Char(
        string="Service order number", default=lambda self: _("New")
    )
    room_id = fields.Many2one(
        comodel_name="hotel.room.type", string="Room number", required=True
    )

    food_lines_ids = fields.Many2many(
        comodel_name="food.product",
        relation="food_and_service_rel",
        column1="room_id",
        column2="food_name",
        string="Food",
        required=True,
    )
    pick_up_location = fields.Char(string="Pick up from")
    pick_up_datetime = fields.Datetime(string="Pick up date and time")
    destination_location = fields.Char(string="Destination")
    car_lines_ids = fields.Many2many(
        comodel_name="transport.vehicle",
        relation="transport_and_service_rel",
        column1="room_id",
        column2="car_brand",
        string="Transport",
        required=True,
    )

    @api.model
    def create(self, value):
        """Inherited create so at time of creation a unique sequence will be generated
        #T00471"""
        value["service_order_number_seq"] = self.env["ir.sequence"].next_by_code(
            "hotel.room.services"
        )
        return super(HotelRoomServices, self).create(value)
