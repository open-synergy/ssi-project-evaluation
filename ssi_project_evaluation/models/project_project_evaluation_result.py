# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProjectProjectEvaluationResult(models.Model):
    _name = "project.project.evaluation_result"
    _description = "project.project - Evaluation Result"

    project_id = fields.Many2one(
        string="Project",
        comodel_name="project.project",
        ondelete="cascade",
        required=True,
    )
    type_id = fields.Many2one(
        string="Evaluation Type",
        comodel_name="project_evaluation_type",
        ondelete="restrict",
        required=True,
    )
    latest_evaluation_id = fields.Many2one(
        string="Latest Evaluation",
        comodel_name="project_evaluation",
        compute="_compute_latest_evaluation_id",
        store=True,
        compute_sudo=True,
    )
    result_id = fields.Many2one(
        string="Result",
        related="latest_evaluation_id.final_result_id",
        store=True,
        compute_sudo=True,
    )
    date = fields.Date(
        related="latest_evaluation_id.date",
        store=True,
        compute_sudo=True,
    )

    previous_evaluation_id = fields.Many2one(
        string="Previous Evaluation",
        comodel_name="project_evaluation",
        compute="_compute_latest_evaluation_id",
        store=True,
        compute_sudo=True,
    )
    previous_result_id = fields.Many2one(
        string="Previous Result",
        related="previous_evaluation_id.final_result_id",
        store=True,
        compute_sudo=True,
    )
    previous_date = fields.Date(
        related="previous_evaluation_id.date",
        store=True,
        compute_sudo=True,
    )
    diff_evaluation = fields.Boolean(
        string="Latest Diff Than Previous",
        compute="_compute_latest_evaluation_id",
        store=True,
        compute_sudo=True,
    )

    @api.depends(
        "project_id",
        "project_id.project_evaluation_ids",
        "project_id.project_evaluation_ids.type_id",
        "project_id.project_evaluation_ids.state",
        "project_id.project_evaluation_ids.final_result_id",
    )
    def _compute_latest_evaluation_id(self):
        for record in self:
            latest = previous = diff = False
            evaluations = record.project_id.project_evaluation_ids.filtered(
                lambda r: r.state == "done" and r.type_id.id == record.type_id.id
            )
            if evaluations:
                latest = evaluations[0]

            if len(evaluations) >= 2:
                previous = evaluations[1]

            if latest != previous and previous:
                diff = True

            record.latest_evaluation_id = latest
            record.previous_evaluation_id = previous
            record.diff_evaluation = diff
