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
        res = super(SaleOrder, self).onchange_partner_id()
        for partner in self.partner_id:
            if not (
                partner.is_delivery_address
                and partner.type == "delivery"
                and partner.company_type == "person"
            ):
                employee_has_set_delivery_addr = self.env["res.partner"].search(
                    [
                        "&",
                        "&",
                        ("id", "in", partner.child_ids.ids),
                        ("is_delivery_address", "=", False),
                        ("type", "=", "delivery"),
                    ]
                )
                self.partner_shipping_id = employee_has_set_delivery_addr[0]
            employee_has_set_is_delivery_addr = self.env["res.partner"].search(
                [
                    "&",
                    ("id", "in", partner.child_ids.ids),
                    ("is_delivery_address", "=", True),
                ]
            )
            self.partner_shipping_id = employee_has_set_is_delivery_addr[0]

        return res
