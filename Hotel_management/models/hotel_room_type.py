from datetime import date

from odoo import _, api, fields, models


class HotelRoomType(models.Model):
    _name = "hotel.room.type"
    _description = "Hotel room type"
    _rec_name = "room_sequence"

    room_sequence = fields.Char(string="Room Number", default=lambda self: _("New"))
    room_type = fields.Selection(
        [
            ("single", "Single"),
            ("double", "Double"),
            ("family", "Family"),
            ("vip", "VIP"),
        ],
        required=True,
    )
    room_price = fields.Float(
        string="Room price", compute="_compute_prices_base_on_seasons"
    )
    room_status = fields.Selection(
        [("vacant", "Vacant"), ("booked", "Booked")],
        default="vacant",
    )
    room_capacity = fields.Integer(
        string="Total room capacity", compute="_compute_room_capacity"
    )
    guests_ids = fields.Many2many(
        comodel_name="res.partner",
        relation="room_with_guests_rel",
        column1="guests_ids",
        column2="name",
        string="Guests",
        required=True,
        readonly=True,
    )
    guests_count = fields.Integer(
        string="Number of guests", compute="_compute_number_of_guests"
    )

    @api.model
    def create(self, value):
        """Inherited create so at time of creation a unique sequence will be generated
        #T00471"""
        value["room_sequence"] = self.env["ir.sequence"].next_by_code("hotel.room.type")
        return super(HotelRoomType, self).create(value)

    @api.onchange("room_type")
    def _compute_room_capacity(self):
        """Function for default values of room capacity for a room type #T00471"""
        for persons in self:
            if persons.room_type == "single":
                persons.room_capacity = 1
            elif persons.room_type == "double":
                persons.room_capacity = 2
            elif persons.room_type == "family":
                persons.room_capacity = 4
            elif persons.room_type == "vip":
                persons.room_capacity = 2

    @api.model
    def name_get(self):
        """overided name_get so that full name of supervisor is Shown #T00471"""
        result = []
        for combined_names in self:
            if combined_names.room_type:
                result.append(
                    (
                        combined_names.id,
                        "%s %s"
                        % (
                            combined_names.room_sequence,
                            combined_names.room_type,
                        ),
                    )
                )
        return result

    @api.depends("guests_ids")
    def _compute_number_of_guests(self):
        """Calculates the total number of guests staying in a room #T00471"""
        for guests in self:
            guests.guests_count = len(guests.guests_ids)

    def action_show_guests(self):
        """action for smart button that shows the guests staying in a room #T00471"""
        return {
            "type": "ir.actions.act_window",
            "name": "Guests",
            "view_mode": "tree",
            "res_model": "res.partner",
            "domain": [("id", "in", self.guests_ids.ids)],
        }

    @api.onchange("room_type")
    def _compute_prices_base_on_seasons(self):
        """compute method to get room prices based on seasons  and multiply the room
        price based on its type #T00471"""
        seasons_dict = {
            "summer": {
                "start": "09-21",
                "end": "12-21",
                "price": float(
                    self.env["ir.config_parameter"].get_param("summer_season_price")
                ),
            },
            "winter": {
                "start": "12-22",
                "end": "04-20",
                "price": float(
                    self.env["ir.config_parameter"].get_param("winter_season_price")
                ),
            },
            "monsoon": {
                "start": "04-21",
                "end": "09-20",
                "price": float(
                    self.env["ir.config_parameter"].get_param("monsoon_season_price")
                ),
            },
        }
        today_date = date.today().strftime("%m-%d")
        for prices in self:
            for _seasons, dates in seasons_dict.items():
                if dates["start"] <= today_date <= dates["end"]:
                    if prices.room_type == "single":
                        prices.room_price = dates["price"] * float(
                            self.env["ir.config_parameter"].get_param(
                                "single_room_price_multiplier"
                            )
                        )
                    elif prices.room_type == "double":
                        prices.room_price = dates["price"] * float(
                            self.env["ir.config_parameter"].get_param(
                                "double_room_price_multiplier"
                            )
                        )
                    elif prices.room_type == "family":
                        prices.room_price = dates["price"] * float(
                            self.env["ir.config_parameter"].get_param(
                                "family_room_price_multiplier"
                            )
                        )
                    elif prices.room_type == "vip":
                        prices.room_price = dates["price"] * float(
                            self.env["ir.config_parameter"].get_param(
                                "vip_room_price_multiplier"
                            )
                        )
