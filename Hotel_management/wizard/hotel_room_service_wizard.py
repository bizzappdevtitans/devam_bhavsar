from odoo import api, fields, models


class HotelRoomServiceWizard(models.TransientModel):
    _name = "hotel.room.service.wizard"
    _description = "Hotel room service wizard"

    service_type = fields.Selection(
        [("food", "Food service"), ("room_keeping", "Room Keeping service")]
    )
    room_id = fields.Many2one(
        comodel_name="hotel.room.type",
        string="Room number",
        default=lambda self: self._default_room_number(),
    )
    food_lines_ids = fields.One2many(
        comodel_name="hotel.room.service.food.line",
        inverse_name="food_service_id",
        string="Food",
    )

    @api.model
    def _default_room_number(self):
        """function to get default name of teacher in wizard #T00348"""
        context = dict(self._context) or {}
        room_no = self.env["hotel.room.type"].browse(context.get("active_id", False))
        return room_no and room_no.id

    def action_order_food_service(self):
        """action to create a food service order #T00471"""
        return self.env["hotel.room.services"].create(
            {
                "room_id": self.room_id.id,
                "service_type": self.service_type,
                "food_lines_ids": [
                    (
                        0,
                        0,
                        {
                            "food_product_id": self.food_lines_ids.food_product_id.ids,
                            "food_price": self.food_lines_ids.food_price,
                            "food_calory": self.food_lines_ids.food_calory,
                            "food_qty": self.food_lines_ids.food_qty,
                            "food_subtotal": self.food_lines_ids.food_subtotal,
                        },
                    )
                ],
            }
        )
