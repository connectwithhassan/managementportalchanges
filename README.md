# TMS (Training Management System)

A Django-based Training Management System for managing students, courses, enrollments, and exams.

## Features

- **Student Management**: Complete student information including personal details, contact info, and status tracking
- **Course Management**: Course details with duration, links, and course head assignment
- **Enrollment Tracking**: Student course enrollments with deadlines and completion tracking
- **Exam Management**: Exam records with marks and percentage calculations
- **Admin Interface**: Comprehensive Django admin interface for all operations

## Models

1. **Student**: Captures comprehensive student information
2. **Course**: Defines course details and duration
3. **CourseEnrolment**: Tracks student course enrollments
4. **Exam**: Records exam details and results

## Setup Instructions

1. **Create Virtual Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run Migrations**:
   ```bash
   python manage.py migrate
   ```

4. **Create Superuser** (if not already created):
   ```bash
   python manage.py createsuperuser
   ```

5. **Populate Sample Data** (optional):
   ```bash
   python manage.py populate_sample_data
   ```

6. **Run Development Server**:
   ```bash
   python manage.py runserver
   ```

7. **Access Admin Interface**:
   - URL: http://127.0.0.1:8000/admin/
   - Username: admin
   - Password: admin123

## Quick Start

Use the provided activation script for easy setup:
```bash
./activate.sh
```

## Database

The project uses SQLite for development (as configured in settings.py).

## Admin Features

- **Student Admin**: View, add, edit students with filtering and search
- **Course Admin**: Manage courses and assign course heads
- **Enrollment Admin**: Track enrollments with calculated extra time
- **Exam Admin**: Record exams with automatic percentage calculation

## Key Features

- **Data Integrity**: Model constraints ensure data consistency
- **Calculated Fields**: Automatic calculation of extra time and exam percentages
- **Comprehensive Admin**: Full CRUD operations through Django admin
- **Search and Filter**: Advanced search and filtering capabilities
- **User-Friendly Interface**: Clean and intuitive admin interface

## Development Notes

- All operations are performed through Django admin interface
- Models include proper validation and constraints
- Calculated properties for extra time and exam percentages
- Foreign key relationships properly configured
- Unique constraints to prevent duplicate enrollments
