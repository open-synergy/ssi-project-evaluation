# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class ProjectEvaluationValueItem(models.Model):
    _name = "project_evaluation_value_item"
    _inherit = ["mixin.master_data"]
    _description = "Project Evaluation Value Item"
