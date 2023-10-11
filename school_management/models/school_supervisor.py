from datetime import date

from odoo import api, fields, models


class SchoolSupervisor(models.Model):
    _name = "school.supervisor"
    _description = "Supervisor details"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _rec_name = "supervisor_first_name"

    supervisor_first_name = fields.Char(string="First Name", required=True)
    supervisor_last_name = fields.Char(string="Last Name ", required=True)
    age_supervisor = fields.Integer(string="Age", compute="_compute_age", store=True)
    gender = fields.Selection(
        [("male", "Male"), ("female", "Female"), ("others", "Others")], string="Gender"
    )
    date_of_birth = fields.Date(string="Date of birth", required=True)
    is_status_check = fields.Boolean(string="Active", default=True, tracking=True)
    supervisor_photo = fields.Image(string="Supervisor photo")
    sequence_supervisor_number = fields.Char(string="Sequential supervisor number")
    email_supervisor = fields.Char(string="Email", tracking=True, help="Must have @")
    assigned_teachers_of_supervisor_ids = fields.One2many(
        comodel_name="school.teacher",
        inverse_name="assigned_supervisor_id",
        string="Teachers",
        tracking=True,
    )
    assigned_principal_id = fields.Many2one(
        comodel_name="school.principal", string="Principal"
    )

    @api.depends("date_of_birth")
    def _compute_age(self):
        """computes the age of supervisor based on date of birth #T00335"""
        for dates in self:
            today = date.today()
            if dates.date_of_birth:
                dates.age_supervisor = today.year - dates.date_of_birth.year

    @api.model
    def create(self, value):
        """inherited create so that at time of record creation there will be a unique
        sequence number for supervisor #T00335"""
        value["sequence_supervisor_number"] = self.env["ir.sequence"].next_by_code(
            "school.supervisor"
        )
        return super(SchoolSupervisor, self).create(value)

    @api.model
    def name_search(self, name, args=None, operator="ilike", limit=100):
        """Inherited name_search so that a supervisor can be searched using fields other
        than name #T00335"""
        args = args or []
        search_name = self.search(
            [
                "|",
                ("sequence_supervisor_number", operator, name),
                ("email_supervisor", operator, name),
            ]
            + args,
            limit=limit,
        )
        if not search_name.ids:
            return super(SchoolSupervisor, self).name_search(
                name=name, args=args, operator=operator, limit=limit
            )
        return search_name.name_get()

    @api.model
    def name_get(self):
        """overided name_get so that full name of supervisor is Shown #T00335"""
        result = []
        for combined_names in self:
            if combined_names.supervisor_last_name:
                result.append(
                    (
                        combined_names.id,
                        "%s %s"
                        % (
                            combined_names.supervisor_first_name,
                            combined_names.supervisor_last_name,
                        ),
                    )
                )
        return result
