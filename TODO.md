# TODO: Change CourseEnrolment Status from Semesters to Levels and Rename Field to Level

- [x] Update core/models.py: Change ENROLMENT_STATUS_CHOICES from semesters to levels
- [x] Rename 'status' field to 'level' in core/models.py
- [x] Update core/admin.py: Change references from 'status' to 'level'
- [x] Create and run Django migration for the field rename
