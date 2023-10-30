from odoo import fields, models


class Project(models.Model):
    _inherit = ["project.project"]

    project_requirements = fields.Char(string="Project requirements")
