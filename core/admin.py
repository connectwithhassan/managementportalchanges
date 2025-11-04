from django.contrib import admin
from django import forms
from .models import Student, Course, CourseEnrolment, Exam


class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter course_enrolment to show only active ones
        if 'course_enrolment' in self.fields:
            self.fields['course_enrolment'].queryset = CourseEnrolment.objects.filter(active_status='Active')


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('serial_number', 'name', 'father_name', 'cnic', 'email', 'contact_number', 'joining_date', 'status')
    list_filter = ('status', 'joining_date', 'resignation_date')
    search_fields = ('serial_number', 'name', 'father_name', 'cnic', 'email', 'contact_number')
    readonly_fields = ('serial_number',)
    fieldsets = (
        ('Basic Information', {
            'fields': ('serial_number', 'name', 'father_name', 'cnic')
        }),
        ('Contact Information', {
            'fields': ('email', 'contact_number', 'address')
        }),
        ('Dates and Status', {
            'fields': ('joining_date', 'resignation_date', 'status')
        }),
    )

    def save_model(self, request, obj, form, change):
        """Auto-generate serial number if not provided"""
        if not obj.serial_number:
            # Generate a unique serial number
            import uuid
            obj.serial_number = f"STU{uuid.uuid4().hex[:6].upper()}"
        super().save_model(request, obj, form, change)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('serial_number', 'course_name', 'course_duration_hours', 'course_head', 'course_link')
    list_filter = ('course_duration_hours', 'course_head')
    search_fields = ('serial_number', 'course_name', 'course_head__name')
    readonly_fields = ('serial_number',)
    fieldsets = (
        ('Course Information', {
            'fields': ('serial_number', 'course_name', 'course_duration_hours', 'course_link')
        }),
        ('Course Head', {
            'fields': ('course_head',)
        }),
    )

    def save_model(self, request, obj, form, change):
        """Auto-generate serial number if not provided"""
        if not obj.serial_number:
            # Generate a unique serial number
            import uuid
            obj.serial_number = f"CRS{uuid.uuid4().hex[:6].upper()}"
        super().save_model(request, obj, form, change)


@admin.register(CourseEnrolment)
class CourseEnrolmentAdmin(admin.ModelAdmin):
    list_display = ('serial_number', 'student', 'course', 'enrolment_date', 'deadline', 'completion_date', 'status', 'active_status', 'extra_time_display')
    list_filter = ('status', 'active_status', 'enrolment_date', 'deadline', 'completion_date', 'course', 'student')
    search_fields = ('serial_number', 'student__name', 'course__course_name')
    readonly_fields = ('serial_number', 'extra_time_display')
    fieldsets = (
        ('Enrolment Information', {
            'fields': ('serial_number', 'student', 'course', 'status', 'active_status')
        }),
        ('Dates', {
            'fields': ('enrolment_date', 'deadline', 'completion_date')
        }),
        ('Calculated Fields', {
            'fields': ('extra_time_display',)
        }),
    )

    def save_model(self, request, obj, form, change):
        """Auto-generate serial number based on student and course"""
        # Only regenerate serial number for new records or if student/course changed
        if not change:  # New record
            if obj.student and obj.course:
                obj.serial_number = f"{obj.student.serial_number}_{obj.course.serial_number}"
            else:
                # Fallback to UUID if student or course not selected
                import uuid
                obj.serial_number = f"ENR{uuid.uuid4().hex[:6].upper()}"
        super().save_model(request, obj, form, change)

    def extra_time_display(self, obj):
        """Display the extra time calculation in the admin"""
        extra_time = obj.extra_time
        if extra_time is not None:
            if extra_time > 0:
                return f"{extra_time} days early"
            elif extra_time < 0:
                return f"{abs(extra_time)} days late"
            else:
                return "On time"
        return "Not completed yet"
    extra_time_display.short_description = "Extra Time"


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    form = ExamForm
    list_display = ('serial_number', 'course_enrolment', 'exam_type', 'exam_date', 'total_marks', 'obtained_marks', 'active_status', 'result_in_percentage_display')
    list_filter = ('exam_type', 'active_status', 'exam_date', 'course_enrolment__course', 'course_enrolment__student')
    search_fields = ('serial_number', 'course_enrolment__student__name', 'course_enrolment__course__course_name')
    readonly_fields = ('serial_number', 'result_in_percentage_display')
    fieldsets = (
        ('Exam Information', {
            'fields': ('serial_number', 'course_enrolment', 'exam_type', 'exam_date', 'active_status')
        }),
        ('Marks', {
            'fields': ('total_marks', 'obtained_marks')
        }),
        ('Calculated Fields', {
            'fields': ('result_in_percentage_display',)
        }),
    )

    def save_model(self, request, obj, form, change):
        """Auto-generate serial number if not provided"""
        if not obj.serial_number:
            # Generate a unique serial number
            import uuid
            obj.serial_number = f"EXM{uuid.uuid4().hex[:6].upper()}"
        super().save_model(request, obj, form, change)

    def result_in_percentage_display(self, obj):
        """Display the percentage result in the admin"""
        return f"{obj.result_in_percentage:.2f}%"
    result_in_percentage_display.short_description = "Result (%)"


# Customize admin site headers
admin.site.site_header = "TMS Administration"
admin.site.site_title = "TMS Admin"
admin.site.index_title = "Welcome to TMS Administration"