"""
TransactionCase test

"""

import logging
import psycopg2.errors
from datetime import timedelta
from odoo import fields
from odoo.exceptions import ValidationError, UserError
from .common import TestCommon
from psycopg2.errors import NotNullViolation

# from psycopg2.errors import NotNullViolation

_logger = logging.getLogger(__name__)


# from odoo import exceptions


class TestSchoollModule(TestCommon):

    def test_01_student_creation_good(self):
        """Test that a student is created with the correct attributes"""
        # Проверяем, что студент был создан
        self.assertTrue(self.student)
        self.assertEqual(self.student.first_name, "first_name_student")
        self.assertEqual(self.student.second_name, "second_name_student")
        self.assertEqual(self.student.last_name, "last_name_student")

    # def test_02_student_creation_bad(self):
    #     """Проверка создания студента с пустыми полями"""
    #     with self.assertRaises(ValidationError):
    #         self.env["hnn_drive_school.student"].create(
    #             {
    #                 "first_name": "",
    #                 "second_name": "Test",
    #                 "last_name": "Student",
    #             }
    #         )

    def test_02_student_creation_bad(self):
        """Проверка создания студента с пустыми полями"""
        with self.assertRaises(ValidationError):
            self.student.id.first_name = ""

    def test_03_student_complaint_compute_name_good(self):
        name_compute = self.student.display_name != ""
        self.assertTrue(name_compute, msg="Complaint name computed")

    def test_04_teacher_creation_good(self):
        """Test that a teacher is created with the correct attributes"""
        self.assertEqual(self.teacher.first_name, "first_name_teacher")
        self.assertEqual(self.teacher.second_name, "second_name_teacher")
        self.assertEqual(self.teacher.last_name, "last_name_teacher")
        self.assertEqual(self.teacher.types_of_instructors, "teacher_instructor")

    def test_05_create_study_group_good(self):
        """create group test"""

        # create group
        sudy_group = self.env["hnn_drive_school.study_group"].create(
            {
                # "student_ids": self.student.id,
                # "student_ids": [(4, self.student.id)],
                "teacher_instructor_id": self.teacher.id,
                "start_date": "2024-10-14",
                "status": "registration",
                "category_id": self.category_a1.id,
                "name": "www-121",
            }
        )
        self.assertTrue(sudy_group.id, "Group should be created successfully")

    # def test_06_create_study_group_without_category_bad(self):
    #     """create bad group test"""

    #     try:
    #         sudy_group_bad = self.env["hnn_drive_school.study_group"].create(
    #             {
    #                 "name": "www-1212",
    #                 # "name": "Group Without Category",
    #                 "teacher_instructor_id": self.teacher.id,
    #                 "start_date": "2024-10-14",
    #                 "status": "registration",
    #             }
    #         )
    #     except (ValidationError, NotNullViolation):
    #         self.fail(
    #             "The sale order should be confirmed, "
    #             "and no ValidationError or NotNullViolation should be raised, "
    #             "for a missing project on the milestone."
    #         )
    # with self.assertRaises(NotNullViolation):

    # dfdff
    # class TestTeacherModel(TestDriveSchoolCommon):
    #     """Test cases for Teacher model"""


#     def test_update_types_of_instructors(self):
#         """Test updating the type of instructor for a teacher"""
#         self.teacher.types_of_instructors = "medical_instructor"
#         self.assertEqual(self.teacher.types_of_instructors, "medical_instructor")

#     def test_compute_all_study_groups(self):
#         """Test _compute_all_study_groups for teacher's study groups"""
#         # Create additional study groups linked to the teacher
#         study_group_teacher = self.env["hnn_drive_school.study_group"].create(
#             {
#                 "name": "Math 101",
#                 "teacher_instructor_id": self.teacher.id,
#             }
#         )
#         study_group_medical = self.env["hnn_drive_school.study_group"].create(
#             {
#                 "name": "First Aid",
#                 "medical_instructor_id": self.teacher.id,
#             }
#         )
#         study_group_driving = self.env["hnn_drive_school.study_group"].create(
#             {
#                 "name": "Driving Basics",
#                 "driving_instructor_id": self.teacher.id,
#             }
#         )

#         # Trigger compute method
#         self.teacher._compute_all_study_groups()

#         # Check that all study groups are included
#         self.assertIn(study_group_teacher, self.teacher.all_study_groups)
#         self.assertIn(study_group_medical, self.teacher.all_study_groups)
#         self.assertIn(study_group_driving, self.teacher.all_study_groups)
#         self.assertEqual(len(self.teacher.all_study_groups), 3)

#     def test_get_report_base_filename(self):
#         """Test report filename generation for a teacher"""
#         expected_filename = "Report by - first_name_teacher last_name_teacher"
#         self.assertEqual(self.teacher._get_report_base_filename(), expected_filename)

#     def test_teacher_as_instructor_types(self):
#         """Test filtering teachers by type of instructor"""
#         # Create different types of teachers
#         medical_instructor = self.env["hnn.drive.school.teacher"].create(
#             {
#                 "first_name": "John",
#                 "last_name": "Doe",
#                 "types_of_instructors": "medical_instructor",
#             }
#         )
#         driving_instructor = self.env["hnn.drive.school.teacher"].create(
#             {
#                 "first_name": "Jane",
#                 "last_name": "Smith",
#                 "types_of_instructors": "driving_instructor",
#             }
#         )

#         # Verify types by searching specific instructors
#         teacher_instructors = self.env["hnn.drive.school.teacher"].search(
#             [("types_of_instructors", "=", "teacher_instructor")]
#         )
#         medical_instructors = self.env["hnn.drive.school.teacher"].search(
#             [("types_of_instructors", "=", "medical_instructor")]
#         )
#         driving_instructors = self.env["hnn.drive.school.teacher"].search(
#             [("types_of_instructors", "=", "driving_instructor")]
#         )

#         self.assertIn(self.teacher, teacher_instructors)
#         self.assertIn(medical_instructor, medical_instructors)
#         self.assertIn(driving_instructor, driving_instructors)
#         self.assertNotIn(self.teacher, medical_instructors)
#         self.assertNotIn(medical_instructor, driving_instructors)
