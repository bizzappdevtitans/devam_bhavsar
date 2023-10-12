from odoo import api, models


class SaleOrder(models.Model):
    _inherit = ["sale.order"]

    @api.onchange("partner_id")
    def onchange_partner_id(self):
        """Inherited this function so that if partner_id is company than check for
        employees which has address type : delivery and set delivery address True.if we
        find more than one employee first employee will be shown if condition is not
        fullfilled then check for employees who has address type : dropship and if we
        get more than one then the first employee will be shown if no condition is
        fullfilled and than the employees who have not selected address type : delivery
        than partner_shipping_id will be the company address #T00460"""
        super(SaleOrder, self).onchange_partner_id()
        company = self.env["res.partner"].browse(self.partner_id.id)
        employees = company.child_ids
        if company and employees:
            if employee_has_set_is_delivery_addr := employees.filtered(
                lambda field: field.is_delivery_address and field.type == "delivery"
            ):
                self.partner_shipping_id = employee_has_set_is_delivery_addr[0]
                if employee_has_set_delivery_addr := employees.filtered(
                    lambda field: employee_has_set_is_delivery_addr is False
                ):
                    self.partner_shipping_id = employee_has_set_delivery_addr[0]
            if employee_has_set_dropship_addr := employees.filtered(
                lambda field: field.is_delivery_address is False
                and field.type == "dropship"
            ):
                self.partner_shipping_id = employee_has_set_dropship_addr[0]
