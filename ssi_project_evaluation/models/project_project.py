# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProjectProject(models.Model):
    _name = "project.project"
    _inherit = "project.project"

    project_evaluation_result_ids = fields.One2many(
        string="Project Evaluation Results",
        comodel_name="project.project.evaluation_result",
        inverse_name="project_id",
        readonly=True,
    )

    project_evaluation_ids = fields.One2many(
        string="Project Evaluations",
        comodel_name="project_evaluation",
        inverse_name="project_id",
        readonly=True,
    )
    evaluation_tag_ids = fields.Many2many(
        string="Evaluation Tags",
        comodel_name="project.tags",
        compute="_compute_evaluation_tag_ids",
        store=True,
        compute_sudo=True,
        relation="rel_project_project_2_evaluation_tag",
        column1="project_id",
        column2="tag_id",
    )

    @api.depends(
        "project_evaluation_result_ids",
        "project_evaluation_result_ids.latest_evaluation_id",
    )
    def _compute_evaluation_tag_ids(self):
        EvaluationResult = self.env["project.project.evaluation_result"]
        for record in self:
            result = []
            criteria = [
                ("project_id", "=", record.id),
            ]
            evaluations = EvaluationResult.search(criteria)
            if len(evaluations) > 0:
                result = evaluations.mapped(
                    "latest_evaluation_id.final_result_id.tag_id"
                )
            record.evaluation_tag_ids = result

    def _get_project_evaluation_result(self, evaluation_type):
        self.ensure_one()
        result = False
        evaluations = self.project_evaluation_result_ids.filtered(
            lambda r: r.type_id.id == evaluation_type.id
        )
        if evaluations:
            result = evaluations[0]

        return result
