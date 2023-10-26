from odoo import api, fields, models


class HotelRoomServiceFood(models.Model):
    _name = "food.product"
    _description = "Hotel room food service"
    _rec_name = "food_name"

    food_name = fields.Char(string="Name of item")
    food_price = fields.Float(string="Price")
    food_calory = fields.Float(string="Calory")
    food_image = fields.Image(string="Food Image")
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
