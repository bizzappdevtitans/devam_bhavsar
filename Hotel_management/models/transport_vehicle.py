from odoo import api, fields, models


class TransportVehicle(models.Model):
    _name = "transport.vehicle"
    _description = "Tranportation vehicles"

    car_model = fields.Char(string="Model")
    car_brand = fields.Char(string="Brand")
    car_type = fields.Selection([("sedan", "Sedan"), ("suv", "SUV")], string="Type")
    car_capacity = fields.Integer(string="Total seats")
    car_image = fields.Image(string="Car Image")

    @api.model
    def name_get(self):
        """overided name_get so that car brand,model and its type is Shown #T00471"""
        result = []
        for combined_names in self:
            if combined_names.car_brand:
                result.append(
                    (
                        combined_names.id,
                        "%s-%s-%s"
                        % (
                            combined_names.car_brand,
                            combined_names.car_model,
                            combined_names.car_type,
                        ),
                    )
                )
        return result
