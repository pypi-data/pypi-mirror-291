# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models
from odoo.tools.safe_eval import safe_eval as eval  # pylint: disable=redefined-builtin


class GeneralAuditWSd4289e4Ratio(models.Model):
    _name = "general_audit_ws_d4289e4.ratio"
    _description = "Preliminary Analytic Procedure - Ratio Analysis (d4289e4) - Ratio"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_d4289e4",
        required=True,
        ondelete="cascade",
    )
    financial_ratio_id = fields.Many2one(
        string="Ratio",
        comodel_name="client_financial_ratio",
        required=True,
    )
    category = fields.Selection(
        string="Category",
        related="financial_ratio_id.category",
    )
    extrapolation_amount = fields.Float(
        string="Extrapolation Amount",
        related=False,
        store=True,
    )
    interim_amount = fields.Float(
        string="Interim Amount",
        related=False,
        store=True,
    )
    previous_amount = fields.Float(
        string="Previous Amount",
        related=False,
        store=True,
    )
    industry_average = fields.Float(
        string="Industry Average",
    )
    analysis = fields.Char(
        string="Analysis",
    )

    def _get_localdict(self):
        self.ensure_one()
        return {
            "env": self.env,
            "document": self,
        }

    def _recompute(self, additional_dict):
        self.ensure_one()
        python_code = self.financial_ratio_id.python_code

        localdict = self._get_localdict()
        localdict.update(additional_dict)
        try:
            eval(
                python_code,
                localdict,
                mode="exec",
                nocopy=True,
            )
            extrapolation_amount = localdict["result_extrapolation"]
            interim_amount = localdict["result_interim"]
            previous_amount = localdict["result_previous"]
            additional_dict.update(
                {
                    self.financial_ratio_id.code: {
                        "extrapolation": extrapolation_amount,
                        "interim": interim_amount,
                        "previous": previous_amount,
                    }
                }
            )
        except Exception:
            extrapolation_amount = interim_amount = previous_amount = 0.0
        self.write(
            {
                "extrapolation_amount": extrapolation_amount,
                "interim_amount": interim_amount,
                "previous_amount": previous_amount,
            }
        )
        return additional_dict
