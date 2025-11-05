# TODO: Implement User Action Logging for Admin Display

- [x] Add ActionLog model to core/models.py
- [x] Add signals for post_save and post_delete on Student, Course, CourseEnrolment, Exam in core/models.py
- [x] Create middleware in core/middleware.py to track current user
- [x] Register ActionLog in core/admin.py with custom admin
- [x] Update TMS/settings.py to include the middleware
- [x] Run makemigrations and migrate
- [x] Test the logging by performing actions (fixed user display)
