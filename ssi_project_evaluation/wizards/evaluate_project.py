# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from datetime import date

from odoo import fields, models


class EvaluateProject(models.TransientModel):
    _name = "evaluate_project"
    _description = "Evaluate Project"

    project_ids = fields.Many2many(
        comodel_name="project.project",
        string="Project",
        required=True,
        relation="evaluate_project_project_rel",
        column1="wizard_id",
        column2="project_id",
        default=lambda self: self._default_project_ids(),
    )
    type_ids = fields.Many2many(
        comodel_name="project_evaluation_type",
        string="Evaluation Types",
        required=True,
        relation="evaluate_project_type_rel",
        column1="wizard_id",
        column2="type_id",
    )

    def _default_project_ids(self):
        active_ids = self.env.context.get("active_ids", [])
        return self.env["project.project"].browse(active_ids)

    def action_confirm(self):
        for record in self.sudo():
            result = record._confirm()
        return result

    def _confirm(self):
        evaluation_ids = []
        for evaluation_type in self.type_ids:
            for project in self.project_ids:
                evaluation = self.env["project_evaluation"].create(
                    {
                        "project_id": project.id,
                        "type_id": evaluation_type.id,
                        "date": date.today(),
                        "date_start": evaluation_type.date_start_offset_id.get_duration(
                            date.today()
                        ),
                        "date_end": evaluation_type.date_end_offset_id.get_duration(
                            date.today()
                        ),
                    }
                )
                evaluation_ids.append(evaluation.id)
        return {
            "name": "Project Evaluations",
            "type": "ir.actions.act_window",
            "res_model": "project_evaluation",
            "view_mode": "tree,form",
            "domain": [("id", "in", evaluation_ids)],
        }
