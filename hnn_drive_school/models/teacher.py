"""
Teacher Module for HNN Drive School

This module defines the Teacher model for the HNN Drive School system. 
It captures all relevant information about instructors, including 
their qualifications, types of instruction they provide, and the 
study groups they are associated with.

"""

import logging

from odoo import models, fields, api


_logger = logging.getLogger(__name__)


class Teacher(models.Model):
    """Model representing a teacher.

    Inherits from the Person model and contains additional fields
    to manage a teacher's qualifications, types of instruction
    they provide, and the study groups they lead.
    """

    _name = "hnn_drive_school.teacher"
    _inherit = "hnn_drive_school.person"

    _description = "Teacher"

    specialist_certificate = fields.Char(string="Specialist Certificate")
    higher_education_info = fields.Char(string="Higher Education Information")

    types_of_instructors = fields.Selection(
        [
            ("driving_instructor", "Driving Instructor"),
            ("teacher_instructor", "Teacher/Instructor"),
            ("medical_instructor", "Medical Instructor"),
        ],
        string="Types of Instructors/Teachers",
    )

    company_id = fields.Many2one(
        comodel_name="res.company",
        required=True,
        readonly=False,
        default=lambda self: self.env.company,
    )

    study_groups_as_teacher = fields.One2many(
        "hnn_drive_school.study_group",
        "teacher_instructor_id",
        string="Study Groups as Teacher",
    )

    study_groups_as_medical_instructor = fields.One2many(
        "hnn_drive_school.study_group",
        "medical_instructor_id",
        string="Study Groups as Medical Instructor",
    )

    study_groups_as_driving_instructor = fields.One2many(
        "hnn_drive_school.study_group",
        "driving_instructor_id",
        string="Study Groups as Driving Instructor",
    )

    all_study_groups = fields.One2many(
        "hnn_drive_school.study_group",
        compute="_compute_all_study_groups",
        string="All Study Groups",
    )

    @api.depends("study_groups_as_teacher", "study_groups_as_medical_instructor")
    def _compute_all_study_groups(self):
        """Computes all study groups associated with the teacher."""
        for teacher in self:
            teacher.all_study_groups = (
                teacher.study_groups_as_teacher
                | teacher.study_groups_as_medical_instructor
                | teacher.study_groups_as_driving_instructor
            )

    # add file link for report
    def _get_report_base_filename(self):
        """Generates the base filename for the teacher's report.
        Returns:
            str: The report filename including
            the teacher's display name.
        """
        self.ensure_one()
        return "Report by - %s" % (self.display_name)
