from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils import timezone
from django.db import models
import os
from django.db import models


class EducationalVideo(models.Model):
    CATEGORY_CHOICES = [
        ('MATH', 'Mathematics'),
        ('SCI', 'Science'),
        ('HIST', 'History'),
        ('LANG', 'Languages'),
        ('COMP', 'Computer Science'),
        ('OTHER', 'Other')
    ]
    GRADE_CHOICES = [
        ('PP1', 'PP1'),
        ('PP2', 'PP2'),
        ('NUR', 'Nursery'),
        ('G1', 'Grade 1'),
        ('G2', 'Grade 2'),
        ('G3', 'Grade 3'),
        ('G4', 'Grade 4'),
        ('G5', 'Grade 5'),
        ('G6', 'Grade 6'),
        ('G7', 'Grade 7'),
        ('G8', 'Grade 8'),
    ]


    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='OTHER')
    video_file = models.FileField(upload_to='educational_videos/')
    thumbnail = models.ImageField(upload_to='educational_thumbnails/', blank=True, null=True)
    study_materials = models.FileField(upload_to='study_materials/', blank=True, null=True)
    worksheet = models.FileField(upload_to='worksheets/', blank=True, null=True)
    instructor = models.CharField(max_length=100)
    duration = models.DurationField(help_text="Duration of the video (HH:MM:SS)", blank=True, null=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    difficulty_level = models.CharField(
        max_length=20,
        choices=[
            ('BEGINNER', 'Beginner'),
            ('INTERMEDIATE', 'Intermediate'),
            ('ADVANCED', 'Advanced')
        ],
        default='BEGINNER'
    )
    grade_level = models.CharField(max_length=3, choices=GRADE_CHOICES)

    def __str__(self):
        return self.title

    def get_video_extension(self):
        """Returns the file extension of the video file."""
        name, extension = os.path.splitext(self.video_file.name)
        return extension[1:].upper() if extension else ''

    def get_study_materials_extension(self):
        """Returns the file extension of study materials."""
        if self.study_materials:
            name, extension = os.path.splitext(self.study_materials.name)
            return extension[1:].upper() if extension else ''
        return ''

    def get_worksheet_extension(self):
        """Returns the file extension of worksheet."""
        if self.worksheet:
            name, extension = os.path.splitext(self.worksheet.name)
            return extension[1:].upper() if extension else ''
        return ''

    def get_duration_display(self):
        """Returns formatted duration string."""
        if self.duration:
            hours = self.duration.seconds // 3600
            minutes = (self.duration.seconds % 3600) // 60
            seconds = self.duration.seconds % 60
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        return "00:00:00"

    def get_grade_display(self):
        """Returns the display name for the grade level"""
        return dict(self.grade_level)


    class Meta:
        ordering = ['-upload_date']




class Course(models.Model):
    assignments = models.ManyToManyField('school.Assignment', blank=True, related_name='courses')
    title = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    instructor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    grade_level = models.CharField(max_length=3, null=True, blank=True)
    subject = models.CharField(max_length=10, null=True, blank=True)
    thumbnail = models.ImageField(upload_to='course_thumbnails/', blank=True, null=True)
    syllabus_file = models.FileField(upload_to='course_syllabi/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    max_students = models.PositiveIntegerField(default=30)

    students = models.ManyToManyField('school.Student', blank=True, related_name='courses', through='school.Enrollment', through_fields=('course', 'student'))

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class SermonNote(models.Model):
    CATEGORY_CHOICES = [
        ('SU', 'Sunday Service'),
        ('MI', 'Midweek Service'),
        ('RE', 'Revival'),
        ('CO', 'Conference'),
        ('YO', 'Youth Service'),
        ('OT', 'Other'),
    ]

    title = models.CharField(max_length=200, null=True, blank=True)
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    preacher = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateField(default=timezone.now)
    scripture_reference = models.CharField(max_length=200, null=True, blank=True)
    category = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default='SU')

    # Main content
    introduction = models.TextField(null=True, blank=True)
    main_points = models.JSONField(default=list)  # Store points as JSON array
    conclusion = models.TextField(null=True, blank=True)

    # Additional fields
    key_verses = models.TextField(blank=True, null=True)
    practical_applications = models.TextField(blank=True, null=True)
    additional_notes = models.TextField(blank=True, null=True)

    # Media attachments
    audio_recording = models.FileField(upload_to='sermon_audio/', blank=True)
    presentation_file = models.FileField(upload_to='sermon_presentations/', blank=True)

    # Metadata
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    tags = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ['-date']
        indexes = [
            models.Index(fields=['date']),
            models.Index(fields=['category']),
        ]

    def __str__(self):
        return f"{self.title} - {self.preacher} ({self.date})"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('services:sermon_note_detail', kwargs={'slug': self.slug})




class SermonComment(models.Model):
    sermon = models.ForeignKey('Sermon', on_delete=models.CASCADE, related_name='sermon_comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Comment by {self.user.username} on {self.sermon.title}'


class SermonTag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name




class Sermon(models.Model):

    sermon_notes = models.FileField(upload_to='sermon_notes/', null=True, blank=True)
    study_materials = models.FileField(upload_to='study_materials/', null=True, blank=True)
    key_points = models.TextField(blank=True)
    title = models.CharField(max_length=200)
    likes = models.IntegerField(default=0)  # Add this new field

    slug = models.SlugField(unique=True)
    description = models.TextField()
    scripture_reference = models.CharField(max_length=200)
    preacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    series = models.ForeignKey(
        'SermonSeries',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sermons'
    )
    date_preached = models.DateField()
    video_file = models.FileField(
        upload_to='sermons/videos/',
        null=True,
        blank=True,
        validators=[FileExtensionValidator(['mp4', 'webm'])]
    )
    audio_file = models.FileField(
        upload_to='sermons/audio/',
        null=True,
        blank=True,
        validators=[FileExtensionValidator(['mp3', 'wav'])]
    )
    presentation_slides = models.FileField(
        upload_to='sermons/slides/',
        null=True,
        blank=True,
        validators=[FileExtensionValidator(['pdf', 'pptx'])]
    )
    thumbnail = models.ImageField(upload_to='sermons/thumbnails/', null=True)
    duration = models.DurationField(null=True, blank=True)
    views = models.PositiveIntegerField(default=0)
    tags = models.ManyToManyField('SermonTag', blank=True)
    is_featured = models.BooleanField(default=False)
    allow_comments = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_preached']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.subject}"


class Subject(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    grade_level = models.CharField(
        max_length=3,
        choices=EducationalVideo.GRADE_CHOICES,
        help_text="Grade level for this subject",
        default='NUR'
    )
    teacher = models.ForeignKey(
        'Teacher',
        on_delete=models.SET_NULL,
        null=True,
        related_name='subjects_taught'
    )
    thumbnail = models.ImageField(
        upload_to='subject_thumbnails/',
        blank=True,
        null=True,
        help_text="Subject cover image"
    )
    syllabus = models.FileField(
        upload_to='subject_syllabi/',
        blank=True,
        null=True,
        help_text="Subject syllabus document"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['grade_level', 'name']

    def __str__(self):
        return f"{self.name} - {self.get_grade_level_display()}"

class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    admission_date = models.DateField(auto_now_add=True)
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('O+', 'O+'), ('O-', 'O-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
    ]
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES)
    parent_name = models.CharField(max_length=100)
    parent_phone = models.CharField(max_length=15)
    parent_email = models.EmailField()
    address = models.TextField()
    GRADE_CHOICES = [
        (0, 'pp one'),
        (0, 'pp two'),
        (0, 'nursery'),
        (1, '6th Grade'),
        (2, '7th Grade'),
        (3, '8th Grade'),
        (4, '6th Grade'),
        (5, '7th Grade'),
        (6, '6th Grade'),
        (7, '7th Grade'),
        (8, '8th Grade')

    ]
    grade = models.IntegerField(choices=GRADE_CHOICES)
    section = models.CharField(max_length=1, choices=[
        ('A', 'Section A'),
        ('B', 'Section B'),
        ('C', 'Section C')
    ])

    class Meta:
        unique_together = ['grade', 'section']
        ordering = ['grade', 'section', 'user__first_name']

    def __str__(self):
        return f"{self.user.get_full_name()} - Grade {self.grade}{self.section}"


class Teacher(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    joining_date = models.DateField(auto_now_add=True)
    courses = models.ManyToManyField(Course, blank=True)
    DEPARTMENT_CHOICES = [
        ('MATH', 'Mathematics'),
        ('SCI', 'Science'),
        ('ENG', 'English'),
        ('SOC', 'Social Studies'),
        ('LANG', 'Languages'),
        ('ARTS', 'Arts'),
        ('PHY', 'Physical Education')
    ]
    department = models.CharField(max_length=4, choices=DEPARTMENT_CHOICES)
    qualification = models.CharField(max_length=200)
    experience_years = models.PositiveIntegerField()
    specialization = models.CharField(max_length=200)

    class Meta:
        ordering = ['department', 'user__first_name']

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.get_department_display()}"


class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrollment_date = models.DateField(auto_now_add=True)
    GRADE_CHOICES = [
        ('A', 'A'), ('B', 'B'), ('C', 'C'),
        ('D', 'D'), ('F', 'F')
    ]
    grade = models.CharField(max_length=1, choices=GRADE_CHOICES, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ['student', 'course']
        ordering = ['-enrollment_date']

    def __str__(self):
        return f"{self.student} - {self.course}"


class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance_records')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField()
    is_present = models.BooleanField(default=True)
    note = models.CharField(max_length=200, blank=True)

    class Meta:
        unique_together = ['student', 'course', 'date']
        ordering = ['-date']

    def __str__(self):
        status = "Present" if self.is_present else "Absent"
        return f"{self.student} - {self.course} - {self.date} ({status})"



class Assignment(models.Model):
    PRIORITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High')
    ]

    title = models.CharField(max_length=200, blank=True, null=True)
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='course_assignments', null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE, related_name='created_assignments', null=True, blank=True)
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE, related_name='assignments', null=True, blank=True)
    students = models.ManyToManyField(
        Student,
        related_name='assignments',
        blank=True
    )
    grade_level = models.CharField(
        max_length=3,
        choices=EducationalVideo.GRADE_CHOICES,
        help_text="Grade level for this assignment"
    )
    priority = models.CharField(max_length=6, choices=PRIORITY_CHOICES, default='MEDIUM')
    file_attachment = models.FileField(upload_to='assignments/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    max_score = models.PositiveIntegerField(default=100)

    class Meta:
        ordering = ['-due_date']

    def __str__(self):
        return self.title if self.title else "Untitled Assignment"

    def get_absolute_url(self):
        return reverse('school:assignment-detail', kwargs={'pk': self.pk})



class AssignmentSubmission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='submissions')
    submitted_at = models.DateTimeField(auto_now_add=True)
    score = models.PositiveIntegerField(null=True, blank=True)
    feedback = models.TextField(blank=True)

    class Meta:
        unique_together = ['assignment', 'student']
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{self.student} - {self.assignment}"




class Resource(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    file = models.FileField(upload_to='resources/')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='resources')
    uploaded_by = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    upload_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-upload_date']

    def __str__(self):
        return self.title


class SermonSeries(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to='sermon_series/thumbnails/', null=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-start_date']
        verbose_name_plural = "Sermon Series"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class SermonCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=50, help_text="Bootstrap icon class name", default="bi-bookmark")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Sermon Categories"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def sermons_count(self):
        return self.sermons.count()