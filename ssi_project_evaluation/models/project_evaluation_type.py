# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import date

from odoo import fields, models


class ProjectEvaluationType(models.Model):
    _name = "project_evaluation_type"
    _description = "Project Evaluation Type"
    _inherit = [
        "mixin.master_data",
        "mixin.many2one_configurator",
    ]

    result_ids = fields.Many2many(
        string="Allowed Results",
        comodel_name="project_evaluation_result",
        relation="rel_project_evaluation_type_2_result",
        column1="type_id",
        column2="result_id",
    )
    result_computation_code = fields.Text(
        string="Result Computation Code",
        required=True,
    )
    question_ids = fields.One2many(
        comodel_name="project_evaluation_type.question",
        inverse_name="type_id",
        string="Questions",
    )
    cron_id = fields.Many2one(
        string="Cron",
        comodel_name="ir.cron",
        readonly=True,
    )
    date_start_offset_id = fields.Many2one(
        string="Start Date Offset",
        comodel_name="base.duration",
    )
    date_end_offset_id = fields.Many2one(
        string="End Date Offset",
        comodel_name="base.duration",
    )

    # Project M2O configurator fields
    project_selection_method = fields.Selection(
        string="Project Selection Method",
        selection=[
            ("manual", "Manual"),
            ("domain", "Domain"),
            ("code", "Python Code"),
        ],
        required=True,
        default="domain",
    )
    project_ids = fields.Many2many(
        comodel_name="project.project",
        string="Projects",
        relation="rel_project_evaluation_type_2_project",
        column1="type_id",
        column2="project_id",
    )
    project_domain = fields.Text(
        string="Project Domain",
        default="[]",
    )
    project_python_code = fields.Text(
        string="Project Python Code",
        default="result = []",
    )

    def action_create_cron(self):
        for record in self.sudo():
            record._create_cron()

    def action_delete_cron(self):
        for record in self.sudo():
            record._delete_cron()

    def _delete_cron(self):
        self.ensure_one()
        self.cron_id.unlink()

    def _create_cron(self):
        self.ensure_one()
        Cron = self.env["ir.cron"]
        name = "Project Batch - Evaluation %s" % (self.name)
        code = """EVType = env["project_evaluation_type"].browse([%s])
EVType._create_batch_evaluation()""" % (
            self.id
        )
        data = {
            "name": name,
            "active": False,
            "model_id": self.env.ref(
                "ssi_project_evaluation.model_project_evaluation_type"
            ).id,
            "interval_number": 1,
            "interval_type": "months",
            "numbercall": -1,
            "code": code,
        }
        cron = Cron.create(data)
        self.write({"cron_id": cron.id})

    def _create_batch_evaluation(self):
        self.ensure_one()
        Batch = self.env["project_batch_evaluation"]
        batch_date = date.today()
        batch_date_start = self.date_start_offset_id.get_duration(batch_date)
        batch_date_end = self.date_end_offset_id.get_duration(batch_date)
        data = {
            "type_id": self.id,
            "date": batch_date,
            "date_start": batch_date_start,
            "date_end": batch_date_end,
        }
        batch = Batch.create(data)
        batch.action_load_project()
