from odoo import fields, models


class Project(models.Model):
    _inherit = ["project.project"]

    # added field in project.project by inherting it to store passed values from SO
    # T00390
    project_requirements = fields.Char(string="Project requirements")
