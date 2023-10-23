from datetime import date

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class HotelRoomReservation(models.Model):
    _name = "hotel.room.reservation"
    _description = "Reserve rooms"
    _inherit = ["mail.thread"]
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
        """Inherited create so at time of creation a unique sequence will be generated
        #T00471"""
        value["reservation_seq"] = self.env["ir.sequence"].next_by_code(
            "hotel.room.reservation"
        )
        return super(HotelRoomReservation, self).create(value)

    def action_confirm(self):
        """action for confirm button #T00471"""
        self.write({"reservation_status": "reserved"})
        room_capacity = 0
        for rooms in self.rooms_ids:
            room_capacity += rooms.room_capacity
        # checks if there are more guests than allowed capacity of room if
        # false raise error
        if not room_capacity >= len(self.customer_ids):
            raise ValidationError(_("Room Capcaity exceeded"))
        mail_template = self.env.ref(
            "Hotel_management.reservation_confirmed_email_template"
        )
        mail_template.send_mail(self.id, force_send=True)
        rooms.write({"room_status": "booked", "guests_ids": self.customer_ids.ids})

    def action_cancel(self):
        """action for cancel button #T00471"""
        self.write({"reservation_status": "cancelled"})
        for rooms in self.rooms_ids:
            rooms.write(
                {
                    "room_status": "vacant",
                    "guests_ids": [(5, 0, 0)],
                }
            )

    def action_cancel_to_draft(self):
        """action to set status to draft after cancellation #T00471"""
        self.write({"reservation_status": "draft"})

    @api.onchange("check_out_date", "check_in_date")
    def _compute_total_days(self):
        """compute method to count total leave days based on check_in_date and
        check_out_date #T00471"""
        for dates in self:
            if dates.check_in_date and dates.check_out_date:
                dates.total_days = (dates.check_out_date - dates.check_in_date).days

    @api.onchange("total_days", "check_in_date")
    def _inverse_calculate_date_from_total_days(self):
        """Inverse of compute method to set check_out_date from check_in_date and
        total_days #T00471"""
        for dates in self:
            if dates.check_in_date and dates.total_days:
                dates.check_out_date = dates.check_in_date + relativedelta(
                    days=dates.total_days
                )

    @api.constrains("total_days")
    def _check_total_days(self):
        """Validates check-in and check-out date by total_days #T00471"""
        if self.total_days < 1:
            raise ValidationError(_("Please enter proper dates"))

    def action_reservation_reminder(self):
        """action for cron job to send reservation reminders #T00471"""
        mail_template = self.env.ref(
            "Hotel_management.reservation_reminder_email_template"
        )
        for reservations in self.get_reservation():
            mail_template.send_mail(reservations.id, force_send=True)

    def get_reservation(self):
        """function to get reservation records for cron job based on filtered conditions
        #T00471"""
        reservations = self.search([]).filtered(
            lambda dates: dates.reservation_status == "reserved"
            and (dates.check_in_date - relativedelta(weeks=1)) == date.today()
        )
        return reservations
