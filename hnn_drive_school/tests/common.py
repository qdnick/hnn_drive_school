from odoo.tests.common import TransactionCase


class TestCommon(TransactionCase):
    """Common setup for all tests"""

    def setUp(self):
        super(TestCommon, self).setUp()

        self.student = self.env["hnn_drive_school.student"].create(
            {
                "first_name": "first_name_student",
                "second_name": "second_name_student",
                "last_name": "last_name_student",
            }
        )

        self.teacher = self.env["hnn_drive_school.teacher"].create(
            {
                "first_name": "first_name_teacher",
                "second_name": "second_name_teacher",
                "last_name": "last_name_teacher",
                "types_of_instructors": "teacher_instructor",
            }
        )

        self.category_a1 = self.env.ref("hnn_drive_school.category_a1")
