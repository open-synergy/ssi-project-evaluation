# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProjectEvaluationResult(models.Model):
    _name = "project_evaluation_result"
    _description = "Project Evaluation Result"
    _inherit = [
        "mixin.master_data",
    ]

    tag_id = fields.Many2one(
        string="Tag",
        comodel_name="project.tags",
        required=True,
    )
