from odoo import fields, models


class Task(models.Model):
    _inherit = ["project.task"]

    # added field in project.task by inherting it to store passed values from SO
    # T00390
    task_requirements = fields.Char(string="Task requirements")
