from django.contrib import admin
from .models import (
    SermonNote, SermonComment, SermonTag, Sermon, Contact, Subject,
    Student, Teacher, Course, Enrollment, Attendance, Assignment,
    AssignmentSubmission, Resource, SermonSeries, SermonCategory
)
from .models import EducationalVideo
from django.contrib import admin
from .models import Course
from django.contrib import admin
from .models import Subject


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'grade_level', 'teacher', 'is_active', 'created_at')
    list_filter = ('grade_level', 'is_active', 'created_at')
    search_fields = ('name', 'description', 'teacher__username')
    date_hierarchy = 'created_at'
    list_per_page = 20

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'grade_level', 'teacher')
        }),
        ('Media Files', {
            'fields': ('thumbnail', 'syllabus'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_active',)
        })
    )

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return ('created_at', 'updated_at')
        return []

    def save_model(self, request, obj, form, change):
        if not change:  # If this is a new object
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'instructor', 'grade_level', 'subject', 'created_at', 'is_active')
    list_filter = ('grade_level', 'subject', 'is_active', 'created_at')
    search_fields = ('title', 'description', 'instructor__username')
    date_hierarchy = 'created_at'
    list_per_page = 20

    fieldsets = (
        ('Course Information', {
            'fields': ('title', 'description', 'instructor', 'grade_level', 'subject')
        }),
        ('Media', {
            'fields': ('thumbnail', 'syllabus_file'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_active',)
        })
    )


@admin.register(EducationalVideo)
class EducationalVideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'instructor', 'category', 'difficulty_level', 'upload_date', 'views', 'likes')
    list_filter = ('category', 'difficulty_level', 'upload_date')
    search_fields = ('title', 'description', 'instructor')
    readonly_fields = ('views', 'likes', 'upload_date')
    date_hierarchy = 'upload_date'
    ordering = ('-upload_date',)

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'instructor', 'category', 'difficulty_level')
        }),
        ('Media Files', {
            'fields': ('video_file', 'thumbnail')
        }),
        ('Learning Materials', {
            'fields': ('study_materials', 'worksheet')
        }),
        ('Statistics', {
            'fields': ('views', 'likes', 'upload_date'),
            'classes': ('collapse',)
        }),
    )

@admin.register(SermonNote)
class SermonNoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'preacher', 'date', 'category', 'is_published')
    list_filter = ('category', 'is_published', 'date')
    search_fields = ('title', 'preacher', 'scripture_reference')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(SermonComment)
class SermonCommentAdmin(admin.ModelAdmin):
    list_display = ('sermon', 'user', 'created_at', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('user__username', 'content')

@admin.register(SermonTag)
class SermonTagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Sermon)
class SermonAdmin(admin.ModelAdmin):
    list_display = ('title', 'preacher', 'date_preached', 'is_featured')
    list_filter = ('is_featured', 'date_preached', 'allow_comments')
    search_fields = ('title', 'description', 'scripture_reference')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at', 'is_resolved')
    list_filter = ('is_resolved', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'grade', 'section', 'admission_date')
    list_filter = ('grade', 'section', 'admission_date')
    search_fields = ('user__username', 'user__email', 'parent_name', 'parent_phone')

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user', 'department', 'qualification', 'experience_years')
    list_filter = ('department', 'joining_date')
    search_fields = ('user__username', 'user__email', 'qualification', 'specialization')



@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'enrollment_date', 'grade', 'is_active')
    list_filter = ('is_active', 'enrollment_date', 'grade')
    search_fields = ('student__user__username', 'course__name')

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'date', 'is_present')
    list_filter = ('is_present', 'date')
    search_fields = ('student__user__username', 'course__name')

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('course', 'title', 'due_date', 'max_score')
    list_filter = ('due_date', 'created_at')
    search_fields = ('title', 'description', 'course__name')

@admin.register(AssignmentSubmission)
class AssignmentSubmissionAdmin(admin.ModelAdmin):
    list_display = ('assignment', 'student', 'submitted_at', 'score')
    list_filter = ('submitted_at',)
    search_fields = ('student__user__username', 'assignment__title')

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'uploaded_by', 'upload_date', 'is_active')
    list_filter = ('is_active', 'upload_date')
    search_fields = ('title', 'description', 'subject__name')

@admin.register(SermonSeries)
class SermonSeriesAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'is_active')
    list_filter = ('is_active', 'start_date')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(SermonCategory)
class SermonCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'is_active', 'sermons_count')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}