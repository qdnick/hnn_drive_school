"""
Tests for different models

"""

import logging

from .common import TestCommon


_logger = logging.getLogger(__name__)


class TestSchoollModule(TestCommon):

    def test_01_student_creation(self):
        """Test that a student is created with the correct attributes"""
        self.assertTrue(self.student)
        self.assertEqual(self.student.first_name, "first_name_student")
        self.assertEqual(self.student.second_name, "second_name_student")
        self.assertEqual(self.student.last_name, "last_name_student")

    def test_02_student_complaint_compute_name_good(self):
        """Test that a correct student compute name"""
        name_compute = self.student.display_name != ""
        self.assertTrue(name_compute, msg="Complaint name computed")

    def test_03_teacher_creation(self):
        """Test that a teacher is created with the correct attributes"""
        self.assertEqual(
            self.teacher.first_name,
            "first_name_teacher",
        )
        self.assertEqual(
            self.teacher.second_name,
            "second_name_teacher",
        )
        self.assertEqual(
            self.teacher.last_name,
            "last_name_teacher",
        )
        self.assertEqual(
            self.teacher.types_of_instructors,
            "teacher_instructor",
        )

    def test_04_create_study_group(self):
        """Сreate group test"""

        sudy_group = self.env["hnn_drive_school.study_group"].create(
            {
                "student_ids": [(4, self.student.id)],
                "teacher_instructor_id": self.teacher.id,
                "start_date": "2024-10-14",
                "status": "registration",
                "category_id": self.category_a1.id,
                "name": "www-121",
            }
        )
        self.assertTrue(
            sudy_group.id,
            "Group should be created successfully",
        )

    def test_05_training_days_update(self):
        """Test updating the 'training_days' field in category"""

        self.category_a1.training_days = 15

        self.assertEqual(self.category_a1.training_days, 15)

    def test_06_generate_teacher_report(self):
        """Test generating the report for a specific teacher"""

        report = self.env.ref(
            "hnn_drive_school.hnn_drive_school_teacher_report",
        )

        report_action = report.report_action(self.teacher)

        self.assertTrue(report_action)

    def test_07_group_report_by_category(self):
        """Test group report wizard filtering by category"""

        wizard = self.env["group.report.wizard"].create(
            {
                "teacher_instructor_id": self.teacher.id,
                "category_id": self.category_a1.id,
            }
        )

        report_action = wizard.generate_report()

        self.assertIsNotNone(
            report_action, "Report generation action should not be None"
        )
