from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class RestaurantReservation(models.Model):
    _name = "restaurant.reservation"
    _description = "Restaurant Booking"
    _rec_name = "reservation_no_seq"

    reservation_no_seq = fields.Char("Reservation No", default=lambda self: _("New"))
    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        required=True,
        default=lambda self: self.env.company,
    )
    guest_name_ids = fields.Many2many(
        comodel_name="res.partner",
        relation="guest_with_restaurant_rel",
        column1="guest_name_ids",
        column2="name",
        string="Guests",
        required=True,
    )
    reservation_date = fields.Datetime(string="Date", required=True)
    room_no_id = fields.Many2one(
        comodel_name="hotel.room.type",
        string="Room Number",
        domain="[('room_status', '=', 'booked')]",
    )
    table_booking_list_ids = fields.Many2many(
        comodel_name="restaurant.tables",
        relation="restaurant_with_table_rel",
        column1="table_booking_list_ids",
        column2="table_no_seq",
        string="Tables",
        required=True,
        domain="[('availability_status', '=', 'available')]",
    )
    restaurant_reservation_states = fields.Selection(
        [
            ("draft", "Draft"),
            ("confirm", "Confirm"),
            ("cancelled", "Cancel"),
        ],
        string="Reservation status",
        readonly=True,
        default="draft",
    )
    is_direct_reservation = fields.Boolean(string="Direct Reservation")
    guest_name = fields.Char(string="Name")
    guest_email = fields.Char(string="Email")
    guest_phone = fields.Integer(string="Phone no.")
    total_guests = fields.Integer(string="Total guests")

    @api.onchange("room_no_id")
    def get_guests_from_room(self):
        if self.room_no_id:
            self.guest_name_ids = self.room_no_id.guests_ids.ids

    def action_confirm(self):
        """action to confirm reservation and send email #T00471"""
        self.write({"restaurant_reservation_states": "confirm"})
        for tables in self.table_booking_list_ids:
            tables.write(
                {
                    "availability_status": "reserved",
                    "restaurant_reservation_ref": self.id,
                }
            )
        if not self.is_direct_reservation:
            mail_template = self.env.ref(
                "Hotel_management.restaurant_guests_reservation_confirmed_email_template"
            )
            mail_template.send_mail(self.id, force_send=True)
        mail_template = self.env.ref(
            "Hotel_management.restaurant_direct_reservation_confirmed_email_template"
        )
        mail_template.send_mail(self.id, force_send=True)

    def action_cancel(self):
        """action to cancel reservation #T00471s"""
        self.write({"restaurant_reservation_states": "cancelled"})
        for tables in self.table_booking_list_ids:
            tables.write(
                {
                    "availability_status": "available",
                }
            )

    def action_cancel_to_draft(self):
        """action to set status to draft after cancellation #T00471"""
        self.write({"restaurant_reservation_states": "draft"})

    @api.model
    def create(self, value):
        """Inherited create so at time of creation a unique sequence will be generated
        #T00471"""
        value["reservation_no_seq"] = self.env["ir.sequence"].next_by_code(
            "restaurant.reservation"
        )
        return super(RestaurantReservation, self).create(value)

    @api.constrains("reservation_date")
    def _check_dates_times(self):
        """checks if the reservation date is proper if false rasie error #T00471"""
        if self.reservation_date < fields.Datetime.now():
            raise ValidationError(_("Please enter proper Reservation Date"))
