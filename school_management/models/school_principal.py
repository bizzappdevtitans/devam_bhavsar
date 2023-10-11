from datetime import date

from odoo import api, fields, models


class SchoolPrincipal(models.Model):
    _name = "school.principal"
    _description = "principal details"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _rec_name = "principal_first_name"

    principal_first_name = fields.Char(string="First Name", required=True)
    principal_last_name = fields.Char(string="Last Name ", required=True)
    age_principal = fields.Integer(string="Age", compute="_compute_age", store=True)
    gender = fields.Selection(
        [("male", "Male"), ("female", "Female"), ("others", "Others")], string="Gender"
    )
    date_of_birth = fields.Date(string="Date of birth", required=True)
    is_status_active = fields.Boolean(string="Active", default=True, tracking=True)
    principal_photo = fields.Image(string="Principal Photo")
    principal_sequence = fields.Char(string="Sequence Number")
    principal_email = fields.Char(string="Email", tracking=True, help="Must have @")
    phone_no_principal = fields.Integer(string="Phone number")
    assigned_supervisors_of_principal_ids = fields.One2many(
        comodel_name="school.supervisor",
        inverse_name="assigned_principal_id",
        string="Supervisors",
    )

    @api.depends("date_of_birth")
    def _compute_age(self):
        """computes the age of principal based on date of birth #T00335"""
        for dates in self:
            today = date.today()
            if dates.date_of_birth:
                dates.age_principal = today.year - dates.date_of_birth.year

    @api.model
    def create(self, value):
        """Inherited create so that at time of record creation there will be a unique
        sequence number for principal #T00335"""
        value["principal_sequence"] = self.env["ir.sequence"].next_by_code(
            "school.principal"
        )
        return super(SchoolPrincipal, self).create(value)

    def action_change_state_to_confirm_info(self):
        """action function to change state if search returns record #T00335"""
        students = self.env["school.student"].search([("is_confirm_info", "=", True)])
        students.write({"admission_state": "confirm_info"})

    def action_change_state_to_confirm_admission(self):
        """action function to change state if search returns record #T00335"""
        students = self.env["school.student"].search(
            [("is_confirm_admission", "=", True)]
        )
        students.write({"admission_state": "admitted"})
