"""
This module manages the study groups within the HNN Drive School,
facilitating the organization and administration of driving
instruction courses. It enables the creation and management of
study groups, linking them to categories, students, and
instructors.
"""

import logging
from datetime import timedelta, date
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


_logger = logging.getLogger(__name__)


class StudyGroup(models.Model):
    """
    Represents a study group within the driving school.

    This model manages information
    about study groups, including
    group status, associated students,
    instructors, and category details.
    """

    _name = "hnn_drive_school.study_group"
    _description = "Study Group"
    _inherit = ["mail.thread"]

    name = fields.Char(string="Group number")

    color = fields.Integer()
    # color = fields.Integer("Color")

    category_id = fields.Many2one(
        "hnn_drive_school.category",
        string="Category",
    )

    student_ids = fields.Many2many(
        "hnn_drive_school.student",
        string="Students",
    )

    student_last_name = fields.Char(
        related="student_ids.last_name",
        string="Student last name",
        store=False,
    )

    student_phone = fields.Char(
        related="student_ids.phone",
        string="Student Phone",
        store=False,
    )

    student_passport_info = fields.Char(
        related="student_ids.passport_info",
        string="Student Passport Info",
        store=False,
    )

    teacher_instructor_id = fields.Many2one(
        "hnn_drive_school.teacher",
        domain="[('types_of_instructors', '=', 'teacher_instructor')]",
        string="Teacher",
    )
    medical_instructor_id = fields.Many2one(
        "hnn_drive_school.teacher",
        domain="[('types_of_instructors', '=', 'medical_instructor')]",
        string="Medical Instructor",
    )

    driving_instructor_id = fields.Many2one(
        "hnn_drive_school.teacher",
        domain="[('types_of_instructors', '=', 'driving_instructor')]",
        string="Driving Instructor",
    )

    status = fields.Selection(
        [
            ("registration", "Registration"),
            ("confirmed", "Confirmed"),
            ("closed", "Closed"),
        ],
        string="Group status",
        default="registration",
        required=True,
    )

    category_detail = fields.Char(
        related="category_id.detail",
        string="Category Detail",
        readonly=True,
        required=True,
    )

    category_full_name = fields.Char(
        related="category_id.full_name",
        string="Category Full Name",
        readonly=True,
        required=True,
    )

    start_date = fields.Date()

    end_date = fields.Date(
        compute="_compute_end_date",
        inverse="_inverse_set_end_date",
        store=True,
    )

    @api.depends("start_date", "category_id.training_days")
    def _compute_end_date(self):
        """
        Computes the end date based on the start date and
        the training days defined in the category.

        Sets the computed end date for the study group.
        """
        for group in self:
            if group.start_date and group.category_id.training_days:
                group.end_date = self._calculate_end_date(
                    group.start_date, group.category_id.training_days
                )

    def _calculate_end_date(self, start_date, days):
        """
        Calculates the end date based on the start date and
        the number of training days, excluding weekends.

        Args:
            start_date (date): The start date of the study group.
            days (int): The number of training days.

        Returns:
            date: The calculated end date.
        """
        end_date = start_date
        days_left = days
        while days_left > 0:
            end_date += timedelta(days=1)
            if end_date.weekday() < 5:
                days_left -= 1
        return end_date

    def _inverse_end_date(self):
        """
        Allows manual setting of the end_date value.

        This method can be used to directly manipulate the
        end_date field from the user interface.
        """
        for group in self:
            group.end_date = group.end_date

    # add inverse metod for changed end_date
    def _inverse_set_end_date(self):
        """
        Placeholder method for inverse calculation of end_date.

        This method is intended to allow updates to the end_date
        but is currently not implemented.
        """
        # pass

    @api.constrains("student_ids")
    def _check_student_minimal_age(self):
        """
        Checks if all students in
        the group meet the minimum age requirement.

        Raises:
            ValidationError: If
            any student does not meet the age requirement.
        """
        for group in self:
            min_minimal_age = group.category_id.minimal_age
            if min_minimal_age:
                for student in group.student_ids:
                    # check student age
                    student_age = (date.today() - student.birth_date).days // 365
                    if student_age < min_minimal_age:
                        raise ValidationError(
                            _(
                                f"Student '{student.last_name}\
                                    ' does not meet the age requirement\
                                        of {min_minimal_age} years "
                                f"for the category \
                                    '{group.category_id.name}'."
                            )
                        )

    # check drive licence
    @api.constrains("student_ids")
    def _check_drivers_license(self):
        """
        Ensures that students have
        a driver's license if required by the category.

        Raises:
            ValidationError: If a student
            is required to have a driver's license but does not.
        """
        for group in self:
            if group.category_id.dependent_category:
                for student in group.student_ids:
                    if not student.drivers_license:
                        raise ValidationError(
                            _(
                                f"Student {student.last_name} "
                                f"must have a driver's license."
                            )
                        )

    @api.constrains("student_ids")
    def _check_driving_experience(self):
        """
        Checks if students have
        the required driving experience.

        Raises:
            ValidationError: If a student does not meet
            the driving experience requirement.
        """
        for group in self:
            if group.category_id.minimal_driving_experience:
                for student in group.student_ids:
                    if (
                        student.drivers_license_date_of_existence
                        < group.category_id.minimal_driving_experience
                    ):
                        raise ValidationError(
                            _(
                                f"Student {student.last_name} must have at least "
                                f"{group.category_id.minimal_driving_experience} years of driving experience."
                            )
                        )

    @api.model
    def write(self, vals):
        """
        Overrides the write method to enforce
        rules based on group status.
        Checks if the user has permission
        to modify a group based on its status.

        Args:
            vals (dict): Values to update the record with.

        Returns:
            bool: The result of the super write call.

        Raises:
            UserError: If a user attempts to modify
            a confirmed or closed group
            without appropriate permissions.
        """
        for record in self:
            if record.status in ("confirmed", "closed"):
                # check manager role
                if not self.env.user.has_group(
                    "hnn_drive_school.group_hnn_drive_school_manager"
                ):
                    raise UserError(
                        _(
                            """You cannot modify a group with
                            status 'Confirmed' or 'Closed'."""
                        )
                    )
            # elif record.status == "registration":
            #     # check user role
            #     if self.env.user.has_group(
            #         "hnn_drive_school.group_hnn_drive_school_user"
            #     ):
            #         pass
        return super(StudyGroup, self).write(vals)
