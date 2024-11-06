# Manifest modules
{
    "name": "Drive school hnn",
    "summary": "",
    "author": "qdnick",
    "category": "Customizations",
    "license": "LGPL-3",
    "version": "17.0.1.0.0",
    "depends": [
        "base",
        "mail",
    ],
    "external_dependencies": {
        "python": [],
    },
    "data": [
        "security/hnn_drive_school_security.xml",
        "security/ir.model.access.csv",
        "wizard/group_report_wizard_views.xml",
        "views/category_views.xml",
        "views/student_views.xml",
        "views/teacher_views.xml",
        "views/study_group_views.xml",
        "views/main_menu_views.xml",
        "data/drive_category.xml",
        "reports/teacher_report.xml",
        "reports/student_report.xml",
        "reports/study_group_report.xml",
    ],
    "demo": [
        "demo/drive_category_training_days.xml",
        "demo/teacher_demo.xml",
        "demo/student_demo.xml",
        "demo/study_group_gemo.xml",
    ],
    "installable": True,
    "auto_install": False,
    "images": ["static/description/icon.png"],
}
