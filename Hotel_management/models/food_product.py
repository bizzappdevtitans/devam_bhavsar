from odoo import fields, models


class HotelRoomServiceFood(models.Model):
    _name = "food.product"
    _description = "Hotel room food service"
    _rec_name = "food_name"

    food_name = fields.Char(string="Name of item")
    food_price = fields.Float(string="Price")
    food_calory = fields.Float(string="Calory")
    food_image = fields.Image(string="Food Image")
