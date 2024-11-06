==================
HNN Drive School Module
==================

"""
This module is designed for managing driving school operations, 
focusing on the organization of study groups, students, and 
instructors. It provides functionalities to handle group 
registration, confirmation, and closure processes, while also 
enforcing various constraints related to student eligibility 
based on age, driving experience, and licensing requirements.

Key Features:
- Manage study groups with specific categories and associated 
  instructors.
- Track students, their contact information, and eligibility 
  criteria.
- Automatically compute group end dates based on start dates 
  and training days.
- Enforce business rules through validation checks, ensuring 
  that students meet age and licensing requirements.
- Role-based access control to prevent unauthorized modifications 
  of group statuses.

This module integrates seamlessly with the Odoo framework and 
utilizes standard Odoo features like models, fields, and 
constraints to provide a robust solution for driving schools.
"""


Installation
============

To install this module, you need to:

#. Clone repository.
#. Add the repository path to the config file.
#. Update the app list.
#. Install the module.


Usage
=====

User manual
-----------

To view the module description, you need to:

* Go to **Apps** > **Apps** > **Main Apps**.

* Search the module by name.

* Open the module form.

Notes:
------

  - Don't forget to update `Apps List` by clicking on `Update Apps List` menu.

Credits
=======

Authors
-------

* Mykola Kharchuk
