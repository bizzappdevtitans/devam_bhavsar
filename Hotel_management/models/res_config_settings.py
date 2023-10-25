from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    summer_season = fields.Float(
        string="Summer season prices", config_parameter="summer_season_price"
    )
    winter_season = fields.Float(
        string="Winter season prices", config_parameter="winter_season_price"
    )
    monsoon_season = fields.Float(
        string="Monsoon season prices", config_parameter="monsoon_season_price"
    )
    single_room = fields.Float(
        string="Single room multiplier", config_parameter="single_room_price_multiplier"
    )
    double_season = fields.Float(
        string="Double room multiplier", config_parameter="double_room_price_multiplier"
    )
    family_season = fields.Float(
        string="Family room multiplier", config_parameter="family_room_price_multiplier"
    )
    vip_season = fields.Float(
        string="VIP room multiplier", config_parameter="vip_room_price_multiplier"
    )
