"""
Wizard model for group reports.

Allows users to set filtering criteria and
generate reports on study groups based on selected
parameters such as status, dates, and teachers.
"""

from odoo import models, fields


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
        string="Teacher: ",
        domain="[('types_of_instructors', '=', 'teacher_instructor')]",
    )

    medical_instructor_id = fields.Many2one(
        "hnn_drive_school.teacher",
        string="Medical instructor: ",
        domain="[('types_of_instructors', '=', 'medical_instructor')]",
    )

    driving_instructor_id = fields.Many2one(
        "hnn_drive_school.teacher",
        string="Driving instructor: ",
        domain="[('types_of_instructors', '=', 'driving_instructor')]",
    )

    category_id = fields.Many2one("hnn_drive_school.category")

    def generate_report(self):
        """
        Generates a report based on the specified filters.

        Filters study groups by status, dates, teachers, and categories
        and returns an action to display the filtered groups.
        """

        domain = []

        # Add filters to domain
        if self.status:
            domain.append(
                (
                    "status",
                    "=",
                    self.status,
                )
            )

        if self.start_date:
            domain.append(
                (
                    "start_date",
                    ">=",
                    self.start_date,
                )
            )

        if self.end_date:
            domain.append(
                (
                    "end_date",
                    "<=",
                    self.end_date,
                )
            )

        if self.teacher_instructor_id:
            domain.append(
                (
                    "teacher_instructor_id",
                    "=",
                    self.teacher_instructor_id.id,
                )
            )

        if self.medical_instructor_id:
            domain.append(
                (
                    "medical_instructor_id",
                    "=",
                    self.medical_instructor_id.id,
                )
            )

        if self.driving_instructor_id:
            domain.append(
                (
                    "driving_instructor_id",
                    "=",
                    self.driving_instructor_id.id,
                )
            )

        # Category filter - only if category is provided
        if self.category_id:
            domain.append(
                (
                    "category_id",
                    "=",
                    self.category_id.id,
                )
            )

        # If no filter is specified, don't add category filter at all
        if not self.category_id:
            # You can add additional logic for default behavior if needed
            pass

        # Search groups based on domain
        groups = self.env["hnn_drive_school.study_group"].search(domain)

        return {
            "type": "ir.actions.act_window",
            "name": "Filtered Groups",
            "res_model": "hnn_drive_school.study_group",
            "view_mode": "tree",
            "domain": [("id", "in", groups.ids)],
            "target": "current",
        }
