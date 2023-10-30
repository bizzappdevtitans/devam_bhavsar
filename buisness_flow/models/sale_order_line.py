from odoo import models


class SaleOrderLine(models.Model):
    _inherit = ["sale.order.line"]

    def _timesheet_create_project_prepare_values(self):
        """Inherited method to pass values from sale order to project #T00390"""
        project_vals = super(
            SaleOrderLine, self
        )._timesheet_create_project_prepare_values()
        project_vals.update(
            {"project_requirements": self.order_id.project_requirements}
        )
        return project_vals

    def _timesheet_create_task_prepare_values(self, project):
        """Inherited method to pass values from sale order to task #T00390"""
        task_vals = super(SaleOrderLine, self)._timesheet_create_task_prepare_values(
            project
        )
        task_vals.update({"task_requirements": self.order_id.task_requirements})
        return task_vals
