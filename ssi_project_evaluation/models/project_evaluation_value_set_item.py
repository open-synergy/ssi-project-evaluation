# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProjectEvaluationValueSetItem(models.Model):
    _name = "project_evaluation_value_set.item"
    _description = "Project Evaluation Value Set - Item"

    set_id = fields.Many2one(
        string="Value Set",
        comodel_name="project_evaluation_value_set",
        required=True,
        ondelete="cascade",
    )
    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=5,
    )
    item_id = fields.Many2one(
        string="Item",
        comodel_name="project_evaluation_value_item",
        required=True,
        ondelete="restrict",
    )
