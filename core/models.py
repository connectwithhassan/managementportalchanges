from django.db import models

# Define choices for the Student Status field
STUDENT_STATUS_CHOICES = [
    ('Active', 'Active'),
    ('Inactive', 'Inactive'),
]

# Define choices for the Course Enrolment Status field
ENROLMENT_STATUS_CHOICES = [
    ('Semester 1', 'Semester 1'),
    ('Semester 2', 'Semester 2'),
    ('Semester 3', 'Semester 3'),
    ('Semester 4', 'Semester 4'),
    # Add more as needed
]

# Define choices for the Active/Inactive Status field
ACTIVE_STATUS_CHOICES = [
    ('Active', 'Active'),
    ('Inactive', 'Inactive'),
]

# Define choices for the Exam Type field
EXAM_TYPE_CHOICES = [
    ('Quiz', 'Quiz'),
    ('Practical', 'Practical'),
    # Add more as needed
]

# 1. Student Model
class Student(models.Model):
    """
    Captures comprehensive information about each student.
    """
    # Serial Number: A unique identifier for the student.
    serial_number = models.CharField(max_length=20, unique=True, primary_key=True)
    # Name: The student's full name.
    name = models.CharField(max_length=100)
    # Father's Name: The student's father's name.
    father_name = models.CharField(max_length=100)
    # CNIC: The student's Computerized National Identity Card number (e.g., XXXXX-XXXXXXX-X).
    cnic = models.CharField(max_length=15, unique=True, help_text="Format: XXXXX-XXXXXXX-X")
    # Email: The student's email address.
    email = models.EmailField(unique=True)
    # Contact Number: The student's contact number, including the country code.
    contact_number = models.CharField(max_length=20)
    # Joining Date: The date the student joined the TMS.
    joining_date = models.DateField()
    # Resignation Date: (Optional) The date the student resigned.
    resignation_date = models.DateField(null=True, blank=True)
    # Address: The student's residential address.
    address = models.TextField()
    # Status: Indicates whether the student is currently active or inactive in the TMS.
    status = models.CharField(max_length=10, choices=STUDENT_STATUS_CHOICES, default='Active')

    def __str__(self):
        return self.name

# 2. Course Model
class Course(models.Model):
    """
    Defines the details of each course offered.
    """
    # Serial Number: A unique identifier for the course.
    serial_number = models.CharField(max_length=20, unique=True, primary_key=True)
    # Course Name: The official name of the course.
    course_name = models.CharField(max_length=150)
    # Course Link: A URL or link related to the course content.
    course_link = models.URLField(max_length=500, null=True, blank=True)
    # Course Duration: The total duration of the course, measured in hours.
    course_duration_hours = models.PositiveIntegerField()
    # Course Head: A foreign key linking to the Student model, identifying the course head.
    # Assuming a student can be designated as a course head.
    course_head = models.ForeignKey(
        Student,
        on_delete=models.SET_NULL, # If the student who is the head leaves, don't delete the course
        related_name='courses_headed',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.course_name

# 3. Course Enrolment Model
class CourseEnrolment(models.Model):
    """
    Tracks the enrolment of students in specific courses.
    """
    # Serial Number: A unique identifier for the enrolment record.
    serial_number = models.CharField(max_length=20, unique=True, primary_key=True)
    # Student: A foreign key linking to the Student model, identifying the enrolled student.
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrolments')
    # Course: A foreign key linking to the Course model, identifying the enrolled course.
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrolments')
    # Enrolment Date: The date the student enrolled in the course.
    enrolment_date = models.DateField()
    # Deadline: The expected completion date for the course.
    deadline = models.DateField()
    # Completion Date: (Optional) The actual date the student completed the course.
    completion_date = models.DateField(null=True, blank=True)
    # Extra Time: Calculated by subtracting the Completion Date from the Deadline.
    # This will be calculated in the application logic or as a model property,
    # but storing it as a field can be useful for caching/reporting.
    # Using DurationField to store time difference (in days/seconds etc.)
    # We will compute the difference in application logic or use a model property.
    # For simplicity in the model definition, we won't define a direct field for the
    # difference but rely on a property/method.
    # Status: Represents the student's progress within the course (e.g., Semester 1, ...).
    status = models.CharField(max_length=50, choices=ENROLMENT_STATUS_CHOICES)
    # Active Status: Indicates whether the enrolment is currently active or inactive.
    active_status = models.CharField(max_length=10, choices=ACTIVE_STATUS_CHOICES, default='Active')

    class Meta:
        # Ensures a student can only be enrolled in a course once (based on FK combination)
        # although the serial_number being primary_key already ensures uniqueness for the record.
        # This is for semantic uniqueness of the relationship.
        unique_together = ('student', 'course')

    @property
    def extra_time(self):
        """
        Calculates the extra time (positive for early, negative for late) in days.
        """
        if self.completion_date and self.deadline:
            # deadline - completion_date: positive if completed early, negative if late.
            time_difference = self.deadline - self.completion_date
            return time_difference.days
        return None

    def __str__(self):
        return f"{self.student.name} enrolled in {self.course.course_name}"

# 4. Exam Model
class Exam(models.Model):
    """
    Records details of exams taken by students in their enrolled courses.
    """
    # Serial Number: A unique identifier for the exam record.
    serial_number = models.CharField(max_length=20, unique=True, primary_key=True)
    # Course Enrolment: A foreign key linking to the Course Enrolment model.
    course_enrolment = models.ForeignKey(
        CourseEnrolment,
        on_delete=models.CASCADE,
        related_name='exams',
        help_text="Links to the specific student-course enrolment."
    )
    # Exam Type: Specifies the type of exam (e.g., Quiz, Practical).
    exam_type = models.CharField(max_length=50, choices=EXAM_TYPE_CHOICES)
    # Exam Date: The date the exam was conducted.
    exam_date = models.DateField()
    # Total Marks: The maximum marks achievable in the exam.
    total_marks = models.DecimalField(max_digits=5, decimal_places=2)
    # Obtained Marks: The marks secured by the student in the exam.
    obtained_marks = models.DecimalField(max_digits=5, decimal_places=2)
    # Active Status: Indicates whether the exam record is currently active or inactive.
    active_status = models.CharField(max_length=10, choices=ACTIVE_STATUS_CHOICES, default='Active')
    # Result in Percentage: The student's exam result, expressed as a percentage.
    # This will be calculated in the application logic or as a model property.
    # For data integrity, we'll make sure obtained_marks <= total_marks
    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(obtained_marks__lte=models.F('total_marks')),
                name='obtained_lte_total_marks'
            )
        ]

    @property
    def result_in_percentage(self):
        """
        Calculates the student's exam result as a percentage.
        """
        if self.total_marks and self.obtained_marks is not None and self.total_marks > 0:
            return (self.obtained_marks / self.total_marks) * 100
        return 0.0

    def __str__(self):
        return f"{self.exam_type} for {self.course_enrolment.student.name} in {self.course_enrolment.course.course_name}"