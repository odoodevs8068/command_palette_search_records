import json
import logging
from odoo import api, models
from odoo.exceptions import AccessError
_logger = logging.getLogger(__name__)


class CommandPaletteRecordSearch(models.AbstractModel):
    _name = "command.palette.record.search"
    _description = "Command Palette Record Search"

    MAX_RESULTS_PER_MODEL = 10
    MAX_TOTAL_RESULTS = 100

    @api.model
    def search_records(self, search_value):
        search_value = (search_value or "").strip()

        if len(search_value) < 2: return []

        params = self.env["ir.config_parameter"].sudo()
        param = params.get_param(
            "command_palette_search_records.search_model_ids",
            default="[]",
        )

        try: model_ids = json.loads(param)
        except (ValueError, TypeError): model_ids = []

        if not isinstance(model_ids, list) or not model_ids: return []

        configured_models = (
            self.env["ir.model"].sudo().browse(model_ids).exists()
        )

        results = []
        for model_config in configured_models:
            if len(results) >= self.MAX_TOTAL_RESULTS:
                break

            model_name = model_config.model

            try: model = self.env[model_name]
            except KeyError: continue

            try: model.check_access_rights("read", raise_exception=True)
            except AccessError: continue

            remaining = self.MAX_TOTAL_RESULTS - len(results)
            limit = min(
                self.MAX_RESULTS_PER_MODEL,
                remaining,
            )

            try:
                records = model.name_search(name=search_value,  operator="ilike", limit=limit)
            except Exception:
                _logger.exception("Command palette search failed for model %s.", model_name)
                continue

            for record_id, record_name in records:
                results.append({
                    "id": record_id,
                    "name": record_name,
                    "model": model_name,
                    "model_name": model_config.name,
                    "description": model._description,
                })
                if len(results) >= self.MAX_TOTAL_RESULTS: break
        return results
