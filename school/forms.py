from django import forms
from .models import Student, Teacher, Course, Enrollment, Attendance, Assignment, AssignmentSubmission
from django import forms
from .models import *
from .models import Contact
from django import forms
from .models import EducationalVideo
from django import forms
from .models import Course
from django import forms
from .models import Subject

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'description', 'grade_level', 'teacher', 'thumbnail', 'syllabus', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter subject name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter subject description'
            }),
            'grade_level': forms.Select(attrs={
                'class': 'form-select'
            }),
            'teacher': forms.Select(attrs={
                'class': 'form-select'
            }),
            'thumbnail': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'syllabus': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'grade_level', 'subject', 'thumbnail', 'syllabus_file']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter course title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter course description'
            }),
            'grade_level': forms.Select(attrs={
                'class': 'form-select'
            }),
            'subject': forms.Select(attrs={
                'class': 'form-select'
            }),
            'thumbnail': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'syllabus_file': forms.FileInput(attrs={
                'class': 'form-control'
            })
        }


class EducationalVideoForm(forms.ModelForm):
    class Meta:
        model = EducationalVideo
        fields = [
            'title',
            'description',
            'category',
            'video_file',
            'thumbnail',
            'study_materials',
            'worksheet',
            'instructor',
            'difficulty_level'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'duration': forms.TimeInput(attrs={'type': 'time', 'step': '1'}),
        }


class SermonCategoryForm(forms.ModelForm):
    class Meta:
        model = SermonCategory
        fields = ['name', 'description', 'icon', 'order', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3})
        }



class SermonCommentForm(forms.ModelForm):
    class Meta:
        model = SermonComment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add a comment...'})
        }

class SermonNoteForm(forms.ModelForm):
    # Convert the JSONField to a more user-friendly textarea
    main_points = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 5,
            'class': 'form-control',
            'placeholder': 'Enter each main point on a new line'
        }),
        help_text="Enter each point on a new line. They will be automatically formatted."
    )

    class Meta:
        model = SermonNote
        fields = [
            'title',
            'preacher',
            'date',
            'scripture_reference',
            'category',
            'introduction',
            'main_points',
            'conclusion',
            'key_verses',
            'practical_applications',
            'additional_notes',
            'audio_recording',
            'presentation_file',
            'tags',
            'is_published'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter sermon title'
            }),
            'preacher': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter preacher name'
            }),
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'scripture_reference': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., John 3:16-17'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'introduction': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter sermon introduction'
            }),
            'conclusion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter sermon conclusion'
            }),
            'key_verses': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter key Bible verses'
            }),
            'practical_applications': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter practical applications'
            }),
            'additional_notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter any additional notes'
            }),
            'tags': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter tags separated by commas'
            }),
            'is_published': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }

    def clean_main_points(self):
        """Convert the textarea input into a list for the JSONField"""
        points = self.cleaned_data['main_points']
        # Split by newlines and remove empty lines
        points_list = [p.strip() for p in points.split('\n') if p.strip()]
        return points_list

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # If we're editing an existing sermon note, convert the JSON list back to newline-separated text
        if self.instance.pk and isinstance(self.instance.main_points, list):
            self.initial['main_points'] = '\n'.join(self.instance.main_points)


class SermonTagForm(forms.ModelForm):
    class Meta:
        model = SermonTag
        fields = ['name']


class SermonForm(forms.ModelForm):
    class Meta:
        model = Sermon
        exclude = ['slug', 'views', 'created_at', 'updated_at']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'date_preached': forms.DateInput(attrs={'type': 'date'}),
            'duration': forms.TimeInput(attrs={'type': 'time', 'step': '1'})
        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4}),
        }



class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['blood_group', 'parent_name', 'parent_phone', 'parent_email',
                  'address', 'grade', 'section']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }


class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['department', 'qualification', 'experience_years', 'specialization']
        widgets = {
            'experience_years': forms.NumberInput(attrs={'min': 0, 'max': 50}),
        }



class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['student', 'course', 'grade', 'is_active']


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['student', 'course', 'date', 'is_present', 'note']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }


class BulkAttendanceForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    course = forms.ModelChoiceField(queryset=Course.objects.all())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'course' in self.data:
            course = Course.objects.get(id=self.data['course'])
            self.fields['students'] = forms.ModelMultipleChoiceField(
                queryset=Student.objects.filter(enrollments__course=course),
                widget=forms.CheckboxSelectMultiple
            )




class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['title', 'description', 'subject', 'due_date', 'grade_level',
                 'priority', 'file_attachment', 'max_score', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'subject': forms.Select(attrs={'class': 'form-select'}),
            'due_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'grade_level': forms.Select(attrs={'class': 'form-select'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'file_attachment': forms.FileInput(attrs={'class': 'form-control'}),
            'max_score': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }


class AssignmentSubmissionForm(forms.ModelForm):
    class Meta:
        model = AssignmentSubmission
        fields = ['assignment', 'student', 'score', 'feedback']
        widgets = {
            'feedback': forms.Textarea(attrs={'rows': 3}),
        }