from odoo import api, fields, models


class HotelRoomServiceFood(models.Model):
    _name = "hotel.room.service.food.line"
    _description = "Hotel room food service lines"

    food_product_id = fields.Many2one(comodel_name="food.product")
    food_service_id = fields.Many2one(comodel_name="hotel.room.services")
    food_price = fields.Float(string="Price", related="food_product_id.food_price")
    food_calory = fields.Float(string="Calory", related="food_product_id.food_calory")
    food_qty = fields.Integer(string="Food Quantity", default=1)
    food_subtotal = fields.Float(string="Subtotal", compute="_compute_total_cost")

    @api.onchange("food_qty")
    def _compute_total_cost(self):
        """compute method to calculate the total price #T00471"""
        for food in self:
            food.update(
                {
                    "food_subtotal": food.food_qty * food.food_price,
                }
            )
