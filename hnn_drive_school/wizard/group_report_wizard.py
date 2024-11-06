"""
Wizard model for group reports.

Allows users to set filtering criteria and
generate reports on study groups based on selected
parameters such as status, dates, and teachers.
"""

from odoo import models, fields, api


class GroupReportWizard(models.TransientModel):
    """
    Allows users to set filtering criteria and
    generate reports on study groups based on selected
    parameters such as status, dates, and teachers.
    """

    _name = "group.report.wizard"
    _description = "Wizard for group Report"

    status = fields.Selection(
        [
            ("registration", "Registration"),
            ("confirmed", "Confirmed"),
            ("closed", "Closed"),
        ],
    )

    start_date = fields.Date(string="Date from: ")

    end_date = fields.Date(string="Date to: ")

    teacher_instructor_id = fields.Many2one(
        "hnn_drive_school.teacher",
        string="Teacher",
        domain="[('types_of_instructors', '=', 'teacher_instructor')]",
    )

    medical_instructor_id = fields.Many2one(
        "hnn_drive_school.teacher",
        string="Teacher",
        domain="[('types_of_instructors', '=', 'medical_instructor')]",
    )

    driving_instructor_id = fields.Many2one(
        "hnn_drive_school.teacher",
        string="Teacher",
        domain="[('types_of_instructors', '=', 'driving_instructor')]",
    )

    category_id = fields.Many2one("hnn_drive_school.category")

    def generate_report(self):
        """
        Generates a report based on the specified filters.

        Filters study groups by status, dates, teachers, and categories
        and returns an action to display the filtered groups.
        """
        # status filter
        groups = self.search([])

        if self.status:
            groups = groups.filtered(lambda g: g.status == self.status)

        # start date filter
        if self.start_date:
            groups = groups.filtered(lambda g: g.start_date >= self.start_date)

        # end date filter
        if self.end_date:
            groups = groups.filtered(lambda g: g.end_date <= self.end_date)

        # teachers filter
        if self.teacher_instructor_id:
            groups = groups.filtered(
                lambda g: g.teacher_instructor_id == self.teacher_instructor_id
            )

        if self.medical_instructor_id:
            groups = groups.filtered(
                lambda g: g.medical_instructor_id == self.medical_instructor_id
            )

        if self.driving_instructor_id:
            groups = groups.filtered(
                lambda g: g.driving_instructor_id == self.driving_instructor_id
            )

        # category filter
        if self.category_id:
            groups = groups.filtered(lambda g: g.category_id == self.category_id)

        return {
            "type": "ir.actions.act_window",
            "name": "Filtered Groups",
            "res_model": "hnn_drive_school.study_group",
            "view_mode": "tree",
            "domain": [("id", "in", groups.ids)],
            "target": "current",
        }
