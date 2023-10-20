from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


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
    room_price = fields.Float(string="Room price")
    room_status = fields.Selection(
        [("vacant", "Vacant"), ("booked", "Booked")],
        default="vacant",
    )
    room_capacity = fields.Integer(string="Total room capacity", default=1)
    guests_ids = fields.Many2many(
        comodel_name="res.partner",
        relation="room_with_guests_rel",
        column1="guests_ids",
        column2="name",
        string="Guests",
        required=True,
        readonly=True,
    )

    @api.model
    def create(self, value):
        value["room_sequence"] = self.env["ir.sequence"].next_by_code("hotel.room.type")
        return super(HotelRoomType, self).create(value)

    @api.constrains("room_capacity")
    def default_capacity_room_type(self):
        for person in self:
            if person.room_type == "single" and person.room_capacity > 1:
                raise ValidationError(_("Room capacity Exceed"))
            if person.room_type == "double" and person.room_capacity > 2:
                raise ValidationError(_("Room capacity Exceed"))
            if person.room_type == "family" and person.room_capacity > 4:
                raise ValidationError(_("Room capacity Exceed"))
            if person.room_type == "vip" and person.room_capacity > 2:
                raise ValidationError(_("Room capacity Exceed"))

    @api.model
    def name_get(self):
        """overided name_get so that full name of supervisor is Shown #T00335"""
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
