# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProjectEvaluationTypeQuestion(models.Model):
    _name = "project_evaluation_type.question"
    _description = "Project Evaluation Type - Question"
    _order = "type_id, sequence"

    type_id = fields.Many2one(
        string="Project Evaluation Type",
        comodel_name="project_evaluation_type",
        required=True,
        ondelete="cascade",
    )
    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=5,
        readonly=True,
    )
    question_type_id = fields.Many2one(
        string="Question Type",
        comodel_name="project_evaluation_question_type",
        required=True,
    )

    def _create_evaluation_question(self, evaluation):
        self.ensure_one()
        self.env["project_evaluation.question"].create(
            {
                "evaluation_id": evaluation.id,
                "sequence": self.sequence,
                "question_type_id": self.question_type_id.id,
            }
        )
