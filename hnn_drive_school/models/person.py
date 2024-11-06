"""
Base Person model for managing 
personal information in the drive school.

This abstract model serves as 
a base for all person-related entities.

Attributes:
    first_name (str): First name of the person.
    second_name (str): Second name of the person.
    last_name (str): Last name of the person.
    phone (str): Phone number of the person.
    birth_date (date): Birth date of the person.
    passport_info (str): Information related to 
    the person's passport.
    tax_id_code (str): Tax ID code of the person.
    drivers_license (str): Driver's license number of the person.
    drivers_license_date_of_issue (date): Date of issue for 
    the driver's license.
    user_id (Many2one): Reference to the user 
    associated with this person.
"""

from odoo import models, fields, api


class Person(models.AbstractModel):
    """
    Abstract model for representing a person in the system.

    This model includes common attributes
    shared by all person-related entities,
    such as students, teachers, and staff.
    """

    _name = "hnn_drive_school.person"
    _description = "Abstract Person"
    _inherit = ["mail.thread"]

    first_name = fields.Char(required=True)
    second_name = fields.Char(required=True)
    last_name = fields.Char(required=True)
    phone = fields.Char(string="Phone number")
    birth_date = fields.Date()
    passport_info = fields.Char()
    tax_id_code = fields.Char(string=" Tax ID Code")
    drivers_license = fields.Char(string="Driver's License")
    drivers_license_date_of_issue = fields.Date()

    # add user id
    user_id = fields.Many2one(
        "res.users",
        string="User",
    )

    @api.depends("last_name", "second_name", "first_name")
    def _compute_display_name(self):
        """Compute the display name by concatenating
        the last name, first name, and second name."""
        for rec in self:
            rec.display_name = (
                f'{rec.last_name or ""} {rec.first_name or ""} {rec.second_name or ""}'
            )
