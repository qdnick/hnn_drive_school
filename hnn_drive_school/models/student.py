"""
Student Module

This module defines the Student model, 
which extends the Person model
and includes specific attributes 
and methods related to students in the drive school.

Attributes:
    medical_certificate (str): 
    Medical certificate information for the student.
    blood_type (str): The blood type of the student.
    group_ids (Many2many): Relation to 
    the study groups the student is enrolled in.
    age (int): Computed age of 
    the student based on the birth date.
    drivers_license_date_of_existence (int): 
    Years since the driver's license was issued.
"""

import logging


from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


_logger = logging.getLogger(__name__)


class Student(models.Model):
    """
    Student model that represents
    a student in the drive school.

    Inherits from the Person model
    and includes additional attributes specific to students,
    such as medical certificates,
    blood type, and their study groups.
    """

    _name = "hnn_drive_school.student"
    _inherit = "hnn_drive_school.person"
    _description = "Student"

    medical_certificate = fields.Char(string="Medical Certificate")
    blood_type = fields.Selection(
        [("a", "A"), ("b", "B"), ("ab", "AB"), ("o", "O")],
        string="Blood Type",
    )
    group_ids = fields.Many2many(
        "hnn_drive_school.study_group",
        string="Study Group",
    )
    age = fields.Integer(compute="_compute_age")

    @api.depends("birth_date")
    def _compute_age(self):
        """Compute the age of the student based on the birth date."""
        for student in self:
            if student.birth_date:
                student.age = fields.Date.today().year - student.birth_date.year
            else:
                student.age = 0

    drivers_license_date_of_existence = fields.Integer(
        compute="_drivers_license_date_of_existence"
    )

    @api.depends("drivers_license_date_of_issue")
    def _drivers_license_date_of_existence(self):
        """Compute the number of years since the driver's license was issued."""
        for student in self:
            if student.drivers_license_date_of_issue:
                student.drivers_license_date_of_existence = (
                    fields.Date.today().year
                    - student.drivers_license_date_of_issue.year
                )
            else:
                student.drivers_license_date_of_existence = 0

    @api.model
    def create(self, vals):
        """
        Override the create method to enforce
        uniqueness of passport info, phone,
        and tax ID code for the student.

        Args:
            vals (dict): The values
            to create the student record.

        Raises:
            ValidationError: If the passport info,
            phone, or tax ID code is not unique.
        """
        if "passport_info" in vals:
            existing_passport = self.search(
                [("passport_info", "=", vals["passport_info"])]
            )
            if existing_passport:
                raise exceptions.ValidationError(_("Passport Info must be unique."))

        if "phone" in vals:
            existing_phone = self.search([("phone", "=", vals["phone"])])
            if existing_phone:
                raise exceptions.ValidationError(_("Phone must be unique."))

        if "tax_id_code" in vals:
            existing_tax_id = self.search([("tax_id_code", "=", vals["tax_id_code"])])
            if existing_tax_id:
                raise exceptions.ValidationError(_("Tax ID Code must be unique."))

        return super(Student, self).create(vals)

    # open student`s groups
    def open_study_groups(self):
        """Open the study groups associated with the student."""
        return {
            "type": "ir.actions.act_window",
            "name": "Groups",
            "view_mode": "tree,form",
            "res_model": "hnn_drive_school.study_group",
            "domain": [("student_ids.id", "=", self.id)],
        }

    # add file link for report
    def _get_report_base_filename(self):
        """Generate the base filename for the
        report based on the student's display name."""
        self.ensure_one()
        return "Report by - %s" % (self.display_name)
