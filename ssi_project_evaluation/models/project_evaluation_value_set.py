# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProjectEvaluationValueSet(models.Model):
    _name = "project_evaluation_value_set"
    _inherit = ["mixin.master_data"]
    _description = "Project Evaluation Value Set"

    value_ids = fields.One2many(
        string="Values",
        comodel_name="project_evaluation_value_set.item",
        inverse_name="set_id",
    )
