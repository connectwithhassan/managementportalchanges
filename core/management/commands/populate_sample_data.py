from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date, timedelta
from core.models import Student, Course, CourseEnrolment, Exam


class Command(BaseCommand):
    help = 'Populate the database with sample data for testing'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')

        # Create sample students
        students_data = [
            {
                'serial_number': 'STU001',
                'name': 'Ahmed Ali',
                'father_name': 'Muhammad Ali',
                'cnic': '12345-1234567-1',
                'email': 'ahmed.ali@example.com',
                'contact_number': '+92-300-1234567',
                'joining_date': date(2024, 1, 15),
                'address': '123 Main Street, Karachi, Pakistan',
                'status': 'Active'
            },
            {
                'serial_number': 'STU002',
                'name': 'Fatima Khan',
                'father_name': 'Hassan Khan',
                'cnic': '12345-1234567-2',
                'email': 'fatima.khan@example.com',
                'contact_number': '+92-300-1234568',
                'joining_date': date(2024, 2, 1),
                'address': '456 Park Avenue, Lahore, Pakistan',
                'status': 'Active'
            },
            {
                'serial_number': 'STU003',
                'name': 'Muhammad Hassan',
                'father_name': 'Ali Hassan',
                'cnic': '12345-1234567-3',
                'email': 'muhammad.hassan@example.com',
                'contact_number': '+92-300-1234569',
                'joining_date': date(2024, 1, 20),
                'address': '789 Garden Road, Islamabad, Pakistan',
                'status': 'Active'
            }
        ]

        students = []
        for student_data in students_data:
            student, created = Student.objects.get_or_create(
                serial_number=student_data['serial_number'],
                defaults=student_data
            )
            students.append(student)
            if created:
                self.stdout.write(f'Created student: {student.name}')

        # Create sample courses
        courses_data = [
            {
                'serial_number': 'CRS001',
                'course_name': 'Python Programming',
                'course_link': 'https://example.com/python-course',
                'course_duration_hours': 40,
                'course_head': students[0]
            },
            {
                'serial_number': 'CRS002',
                'course_name': 'Web Development',
                'course_link': 'https://example.com/web-dev-course',
                'course_duration_hours': 60,
                'course_head': students[1]
            },
            {
                'serial_number': 'CRS003',
                'course_name': 'Database Management',
                'course_link': 'https://example.com/database-course',
                'course_duration_hours': 30,
                'course_head': students[2]
            }
        ]

        courses = []
        for course_data in courses_data:
            course, created = Course.objects.get_or_create(
                serial_number=course_data['serial_number'],
                defaults=course_data
            )
            courses.append(course)
            if created:
                self.stdout.write(f'Created course: {course.course_name}')

        # Create sample enrollments
        enrollments_data = [
            {
                'serial_number': 'ENR001',
                'student': students[0],
                'course': courses[0],
                'enrolment_date': date(2024, 1, 20),
                'deadline': date(2024, 3, 20),
                'completion_date': date(2024, 3, 15),
                'status': 'Semester 1',
                'active_status': 'Active'
            },
            {
                'serial_number': 'ENR002',
                'student': students[1],
                'course': courses[1],
                'enrolment_date': date(2024, 2, 5),
                'deadline': date(2024, 4, 5),
                'completion_date': None,
                'status': 'Semester 2',
                'active_status': 'Active'
            },
            {
                'serial_number': 'ENR003',
                'student': students[2],
                'course': courses[2],
                'enrolment_date': date(2024, 1, 25),
                'deadline': date(2024, 3, 25),
                'completion_date': date(2024, 3, 30),
                'status': 'Semester 1',
                'active_status': 'Inactive'
            }
        ]

        enrollments = []
        for enrollment_data in enrollments_data:
            enrollment, created = CourseEnrolment.objects.get_or_create(
                serial_number=enrollment_data['serial_number'],
                defaults=enrollment_data
            )
            enrollments.append(enrollment)
            if created:
                self.stdout.write(f'Created enrollment: {enrollment.student.name} in {enrollment.course.course_name}')

        # Create sample exams
        exams_data = [
            {
                'serial_number': 'EXM001',
                'course_enrolment': enrollments[0],
                'exam_type': 'Quiz',
                'exam_date': date(2024, 2, 15),
                'total_marks': 50.00,
                'obtained_marks': 45.00,
                'active_status': 'Active'
            },
            {
                'serial_number': 'EXM002',
                'course_enrolment': enrollments[0],
                'exam_type': 'Practical',
                'exam_date': date(2024, 3, 10),
                'total_marks': 100.00,
                'obtained_marks': 85.00,
                'active_status': 'Active'
            },
            {
                'serial_number': 'EXM003',
                'course_enrolment': enrollments[1],
                'exam_type': 'Quiz',
                'exam_date': date(2024, 3, 1),
                'total_marks': 30.00,
                'obtained_marks': 28.00,
                'active_status': 'Inactive'
            }
        ]

        for exam_data in exams_data:
            exam, created = Exam.objects.get_or_create(
                serial_number=exam_data['serial_number'],
                defaults=exam_data
            )
            if created:
                self.stdout.write(f'Created exam: {exam.exam_type} for {exam.course_enrolment.student.name}')

        self.stdout.write(
            self.style.SUCCESS('Successfully populated database with sample data!')
        )
        self.stdout.write('You can now access the admin interface at http://127.0.0.1:8000/admin/')
        self.stdout.write('Username: admin, Password: admin123')
