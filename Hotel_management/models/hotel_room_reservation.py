from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models


class HotelRoomReservation(models.Model):
    _name = "hotel.room.reservation"
    _description = "Reserve rooms"
    _rec_name = "reservation_seq"

    reservation_seq = fields.Char(string="Room Number", default=lambda self: _("New"))
    customer_ids = fields.Many2many(
        comodel_name="res.partner",
        relation="guest_with_room_rel",
        column1="customer_ids",
        column2="name",
        string="Guests",
        required=True,
    )
    rooms_ids = fields.Many2many(
        comodel_name="hotel.room.type",
        relation="customer_room_rel",
        column1="customer_ids",
        column2="room_sequence",
        string="Rooms",
        domain="[('room_status', '=', 'vacant')]",
        required=True,
    )
    reservation_status = fields.Selection(
        [("draft", "Draft"), ("reserved", "Reserved"), ("cancelled", "Cancelled")],
        default="draft",
    )
    check_in_date = fields.Date(string="Check in on", required=True)
    check_out_date = fields.Date(string="Check out on", required=True)
    total_days = fields.Integer(
        string="Total staying days",
        compute="_compute_total_days",
        inverse="_inverse_calculate_date_from_total_days",
        required=True,
    )

    @api.model
    def create(self, value):
        value["reservation_seq"] = self.env["ir.sequence"].next_by_code(
            "hotel.room.reservation"
        )
        return super(HotelRoomReservation, self).create(value)

    def action_confirm(self):
        self.write({"reservation_status": "reserved"})
        for rooms in self.rooms_ids:
            rooms.write({"room_status": "booked", "guests_ids": self.customer_ids.ids})

    def action_cancel(self):
        self.write({"reservation_status": "cancelled"})
        for rooms in self.rooms_ids:
            rooms.write(
                {
                    "room_status": "vacant",
                    "guests_ids": [(5, 0, 0)],
                }
            )

    @api.onchange("check_out_date", "check_in_date")
    def _compute_total_days(self):
        """compute method to count total leave days based on check_in_date and
        check_out_date #T00435"""
        for dates in self:
            if dates.check_in_date and dates.check_out_date:
                dates.total_days = (dates.check_out_date - dates.check_in_date).days

    @api.onchange("total_days", "check_in_date")
    def _inverse_calculate_date_from_total_days(self):
        """Inverse of compute method to set check_out_date from check_in_date and
        total_days #T00435"""
        for dates in self:
            if dates.check_in_date and dates.total_days:
                dates.check_out_date = dates.check_in_date + relativedelta(
                    days=dates.total_days
                )
