import json
from odoo import api, fields, models

class ResConfigSettingsInherit(models.TransientModel):
    _inherit = "res.config.settings"

    search_model_ids = fields.Many2many("ir.model", string="Command Palette Search Models")

    def set_values(self):
        res = super().set_values()
        self.env["ir.config_parameter"].sudo().set_param(
            "command_palette_search_records.search_model_ids",
            json.dumps(self.search_model_ids.ids),
        )
        return res

    @api.model
    def get_values(self):
        res = super().get_values()
        params = self.env["ir.config_parameter"].sudo()
        param = params.get_param(
            "command_palette_search_records.search_model_ids",
            default="[]",
        )
        try:  model_ids = json.loads(param)
        except (ValueError, TypeError): model_ids = []
        if not isinstance(model_ids, list): model_ids = []
        res.update({"search_model_ids": [(6, 0, model_ids)]})
        return res