"""
Category model for managing categories in the drive school.

Attributes:
    name (str): Name of the category.
    training_days (int): Number of training days for the category.
    detail (str): Additional details about the category, translatable.
    description (str): Description of the category, translatable.
    minimal_age (int): Minimum age requirement for the category.
    dependent_category (Many2one): Reference to a dependent category.
    minimal_driving_experience (int): Minimum driving experience required.
    full_name (str): Full name composed of name and detail fields.
"""

from odoo import models, fields, api


class Category(models.Model):

    _name = "hnn_drive_school.category"
    _description = "Category"

    name = fields.Char(required=True)
    training_days = fields.Integer(string="Number of Training Days")
    detail = fields.Char(translate=True)
    description = fields.Char(translate=True)
    minimal_age = fields.Integer()

    dependent_category = fields.Many2one(
        "hnn_drive_school.category",
        ondelete="set null",
    )
    minimal_driving_experience = fields.Integer()

    full_name = fields.Char(
        compute="_compute_full_name",
        store=True,
        # translate=True,
    )

    @api.depends("name", "detail")
    def _compute_full_name(self):
        """Compute the full name by concatenating the name and detail fields"""
        for rec in self:
            rec.full_name = f'{rec.name or ""} {rec.detail or ""}'

    # @api.depends("name", "detail")
    # def _compute_full_name(self):
    #     """Compute the full name by concatenating the name and detail fields"""
    #     for rec in self:
    #         lang_ids = rec.env["res.lang"].get_installed()
    #         for lang in lang_ids:
    #             rec_lang = rec.with_context(lang=lang.code)
    #             rec_lang.full_name = f'{rec_lang.name or ""} {rec_lang.detail or ""}'

    # @api.model
    # def create(self, vals):
    #     record = super().create(vals)
    #     record._compute_full_name()  # Принудительно вычислить full_name при создании записи
    #     return record

    # def write(self, vals):
    #     res = super().write(vals)
    #     for rec in self:
    #         rec._compute_full_name()  # Принудительно вычислить full_name при изменении записи
    #     return res
