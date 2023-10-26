from odoo import api, fields, models


class HotelRoomServiceWizard(models.TransientModel):
    _name = "hotel.room.service.wizard"
    _description = "Hotel room service wizard"

    service_type = fields.Selection(
        [("food", "Food service"), ("transport", "Transportation service")]
    )
    room_id = fields.Many2one(
        comodel_name="hotel.room.type",
        string="Room number",
        default=lambda self: self._default_room_number(),
    )
    food_lines_ids = fields.Many2many(
        comodel_name="food.product",
        relation="food_and_service_wizard_rel",
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
        relation="transport_and_service_wizard_rel",
        column1="room_id",
        column2="car_brand",
        string="Transport",
        required=True,
    )

    @api.model
    def _default_room_number(self):
        """function to get default name of teacher in wizard #T00348"""
        context = dict(self._context) or {}
        room_no = self.env["hotel.room.type"].browse(context.get("active_id", False))
        return room_no and room_no.id

    def action_order_service(self):
        """action to create a food service order #T00471"""
        if not self.service_type == "food":
            self.env["hotel.room.services"].create(
                {
                    "pick_up_location": self.pick_up_location,
                    "pick_up_datetime": self.pick_up_datetime,
                    "destination_location": self.destination_location,
                    "room_id": self.room_id.id,
                    "service_type": self.service_type,
                    "car_lines_ids": self.car_lines_ids.ids,
                }
            )
        self.env["hotel.room.services"].create(
            {
                "room_id": self.room_id.id,
                "service_type": self.service_type,
                "food_lines_ids": self.food_lines_ids.ids,
            }
        )
