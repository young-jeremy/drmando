from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import *
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Avg, Count, Q
from .models import (Student, Teacher, Course, Enrollment,
                     Attendance, Assignment, AssignmentSubmission, Sermon)
from .forms import (StudentForm, TeacherForm, CourseForm, EnrollmentForm,
                    AttendanceForm, BulkAttendanceForm, AssignmentForm,
                    AssignmentSubmissionForm, SermonForm, SermonCategoryForm)

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Avg, Count
from .models import (Student, Teacher, Course, Enrollment,
                     Attendance, Assignment, AssignmentSubmission)
from .forms import (StudentForm, TeacherForm, CourseForm, EnrollmentForm,
                    AttendanceForm, BulkAttendanceForm, AssignmentForm,
                    AssignmentSubmissionForm)
from django.views.generic import ListView, DetailView
from .models import Subject
from django.views.generic import ListView, DetailView, CreateView
from .models import Resource
from django.views.generic import CreateView
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Avg, Count
from .forms import ContactForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import EducationalVideo
from .forms import EducationalVideoForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CourseForm
from .models import Course
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from .models import Subject
from .forms import SubjectForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from .models import Subject
from .forms import SubjectForm


@login_required
def subject_edit(request, pk):
    """
    View for editing an existing subject.
    Requires staff/teacher permissions.
    """
    subject = get_object_or_404(Subject, pk=pk)

    # Check permissions
    if not (request.user.is_staff or hasattr(request.user, 'teacher')):
        messages.error(request, "You don't have permission to edit subjects.")
        return redirect('school:subject-detail', pk=subject.pk)

    if request.method == 'POST':
        form = SubjectForm(request.POST, request.FILES, instance=subject)
        if form.is_valid():
            # Save the form but don't commit yet
            subject = form.save(commit=False)

            # Handle file uploads
            if 'thumbnail' in request.FILES:
                # Delete old thumbnail if it exists
                if subject.thumbnail:
                    subject.thumbnail.delete(save=False)
                subject.thumbnail = request.FILES['thumbnail']

            if 'syllabus' in request.FILES:
                # Delete old syllabus if it exists
                if subject.syllabus:
                    subject.syllabus.delete(save=False)
                subject.syllabus = request.FILES['syllabus']

            # Save the subject
            subject.save()

            messages.success(request, 'Subject updated successfully!')
            return redirect('school:subject-detail', pk=subject.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = SubjectForm(instance=subject)

    context = {
        'form': form,
        'subject': subject,
        'title': f'Edit Subject: {subject.name}',
        'is_edit': True,
        'can_delete': request.user.is_staff,  # Only staff can delete subjects
    }

    return render(request, 'school/subject_edit.html', context)


@login_required
def subject_toggle_status(request, pk):
    """
    View for toggling subject active status.
    Requires staff permissions.
    """
    subject = get_object_or_404(Subject, pk=pk)

    if not request.user.is_staff:
        messages.error(request, "You don't have permission to modify subjects.")
        return redirect('school:subject-detail', pk=subject.pk)

    subject.is_active = not subject.is_active
    subject.save()

    status = "activated" if subject.is_active else "deactivated"
    messages.success(request, f'Subject {status} successfully!')

    return redirect('school:subject-detail', pk=subject.pk)


@login_required
def subject_delete_file(request, pk, file_type):
    """
    View for deleting subject files (thumbnail or syllabus).
    Requires staff/teacher permissions.
    """
    subject = get_object_or_404(Subject, pk=pk)

    if not (request.user.is_staff or hasattr(request.user, 'teacher')):
        messages.error(request, "You don't have permission to modify subjects.")
        return redirect('school:subject-detail', pk=subject.pk)

    if file_type == 'thumbnail' and subject.thumbnail:
        subject.thumbnail.delete()
        messages.success(request, 'Thumbnail removed successfully!')
    elif file_type == 'syllabus' and subject.syllabus:
        subject.syllabus.delete()
        messages.success(request, 'Syllabus removed successfully!')

    return redirect('school:subject-edit', pk=subject.pk)



@login_required
def subject_create(request):
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to create subjects.")
        return redirect('school:subject-list')

    if request.method == 'POST':
        form = SubjectForm(request.POST, request.FILES)
        if form.is_valid():
            subject = form.save()
            messages.success(request, 'Subject created successfully!')
            return redirect('school:subject-detail', pk=subject.pk)
    else:
        form = SubjectForm()

    return render(request, 'school/subject_create.html', {
        'form': form,
        'title': 'Create New Subject'
    })


@login_required
def subject_edit(request, pk):
    subject = get_object_or_404(Subject, pk=pk)

    # Check permissions
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to edit subjects.")
        return redirect('school:subject-detail', pk=subject.pk)

    if request.method == 'POST':
        form = SubjectForm(request.POST, request.FILES, instance=subject)
        if form.is_valid():
            subject = form.save()
            messages.success(request, 'Subject updated successfully!')
            return redirect('school:subject-detail', pk=subject.pk)
    else:
        form = SubjectForm(instance=subject)

    return render(request, 'school/subjects/subject_create.html', {
        'form': form,
        'subject': subject,
        'title': f'Edit Subject: {subject.name}'
    })


@login_required
def subject_delete(request, pk):
    subject = get_object_or_404(Subject, pk=pk)

    # Check permissions
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to delete subjects.")
        return redirect('school:subject-detail', pk=subject.pk)

    if request.method == 'POST':
        subject.delete()
        messages.success(request, 'Subject deleted successfully!')
        return redirect('school:subject-list')

    return render(request, 'school/subject_delete.html', {
        'subject': subject
    })


@login_required
def subject_toggle_status(request, pk):
    subject = get_object_or_404(Subject, pk=pk)

    # Check permissions
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to modify subjects.")
        return redirect('school:subject-detail', pk=subject.pk)

    subject.is_active = not subject.is_active
    subject.save()

    status = "activated" if subject.is_active else "deactivated"
    messages.success(request, f'Subject {status} successfully!')

    return redirect('school:subject-detail', pk=subject.pk)



@login_required
def create_course(request):
    if not (request.user.is_staff or hasattr(request.user, 'teacher')):
        messages.error(request, "You don't have permission to create courses.")
        return redirect('home')

    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.instructor = request.user
            course.save()
            messages.success(request, 'Course created successfully!')
            return redirect('school:course_detail', pk=course.pk)
    else:
        form = CourseForm()

    return render(request, 'school/courses/create_course.html', {
        'form': form,
        'title': 'Create New Course'
    })

def video_list(request):
    category = request.GET.get('category')
    difficulty = request.GET.get('difficulty')

    videos = EducationalVideo.objects.all()

    if category:
        videos = videos.filter(category=category)
    if difficulty:
        videos = videos.filter(difficulty_level=difficulty)

    paginator = Paginator(videos, 12)  # Show 12 videos per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'categories': EducationalVideo.CATEGORY_CHOICES
    }
    return render(request, 'school/educational/video_list.html', context)



def video_detail(request, video_id):
    video = get_object_or_404(EducationalVideo, id=video_id)
    # Increment view count
    video.views += 1
    video.save()
    return render(request, 'school/educational/video_detail.html', {'video': video})


@login_required
def upload_video(request):
    if request.method == 'POST':
        form = EducationalVideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save()
            return redirect('school:video_detail', video_id=video.id)
    else:
        form = EducationalVideoForm()
    return render(request, 'school/educational/video_upload.html', {'form': form})


@login_required
def edit_video(request, video_id):
    video = get_object_or_404(EducationalVideo, id=video_id)
    if request.method == 'POST':
        form = EducationalVideoForm(request.POST, request.FILES, instance=video)
        if form.is_valid():
            form.save()
            return redirect('school:video_detail', video_id=video.id)
    else:
        form = EducationalVideoForm(instance=video)
    return render(request, 'school/educational/video_edit.html', {'form': form, 'video': video})


@login_required
def like_video(request, video_id):
    if request.method == 'POST':
        video = get_object_or_404(EducationalVideo, id=video_id)
        video.likes += 1
        video.save()
        return redirect('school:video_detail', video_id=video.id)



@login_required
def save_note(request, sermon_slug):
    if request.method == 'POST':
        sermon = get_object_or_404(Sermon, slug=sermon_slug)
        note = SermonNote.objects.create(
            sermon=sermon,
            user=request.user,
            content=request.POST.get('content')
        )
        messages.success(request, 'Note saved successfully!')
    return redirect('school:sermon_details', sermon_slug=sermon_slug)

def sermon_categories(request):
    categories = SermonCategory.objects.all()
    return render(request, 'school/sermons/categories.html', {'categories': categories})

@login_required
def edit_sermon_category(request, category_slug):
    category = get_object_or_404(SermonCategory, slug=category_slug)
    if request.method == 'POST':
        form = SermonCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('services:categories')
    else:
        form = SermonCategoryForm(instance=category)
    return render(request, 'school/sermons/edit_category.html', {'form': form})

@login_required
def delete_sermon_category(request, category_slug):
    category = get_object_or_404(SermonCategory, slug=category_slug)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully!')
    return redirect('services:categories')



@login_required
def sermon_list(request):
    # Change ordering from 'date' to 'date_preached'
    sermons = Sermon.objects.all().order_by('-date_preached')

    # Filter by search query if provided
    search_query = request.GET.get('search', '')
    if search_query:
        sermons = sermons.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(scripture_reference__icontains=search_query)
        )

    # Filter by category if provided
    category_id = request.GET.get('category')
    if category_id:
        sermons = sermons.filter(series__category_id=category_id)

    # Pagination
    paginator = Paginator(sermons, 12)  # Show 12 sermons per page
    page = request.GET.get('page')
    sermons = paginator.get_page(page)

    # Get categories for filter dropdown
    categories = SermonCategory.objects.all()

    context = {
        'sermons': sermons,
        'categories': categories,
        'search_query': search_query,
        'current_category': category_id
    }
    return render(request, 'school/sermons/home_sermons.html', context)


@login_required
def sermon_detail(request, sermon_slug):
    sermon = get_object_or_404(Sermon, slug=sermon_slug)

    # Get related sermons from same series or by same preacher
    related_sermons = Sermon.objects.filter(
        Q(series=sermon.series) | Q(preacher=sermon.preacher)
    ).exclude(id=sermon.id).order_by('-date_preached')[:3]

    context = {
        'sermon': sermon,
        'related_sermons': related_sermons,
        'user_has_liked': Sermon.objects.filter(id=request.user.id).exists()
    }
    return render(request, 'school/sermons/sermon_detail.html', context)


@login_required
def like_sermon(request, sermon_slug):
    sermon = get_object_or_404(Sermon, slug=sermon_slug)
    if request.user in sermon.likes.all():
        sermon.likes.remove(request.user)
        liked = False
    else:
        sermon.likes.add(request.user)
        liked = True
    return JsonResponse({'liked': liked, 'count': sermon.likes.count()})



def add_sermon_view(request):
    if request.method == 'POST':
        form = SermonForm()
        if form.is_valid():
            sermon = form.save()
            # Use the correct URL name
        return redirect('school:sermon_list', video_id=sermon.id)
    # ... rest of your view code ...



class PrivacyView(TemplateView):
    template_name = 'school/privacy.html'



class ContactView(CreateView):
    template_name = 'school/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('school:contact')

    def form_valid(self, form):
        messages.success(self.request, 'Thank you for your message. We will get back to you soon!')
        return super().form_valid(form)


class AboutView(TemplateView):
    template_name = 'school/about.html'




class ResourceListView(LoginRequiredMixin, ListView):
    model = Resource
    template_name = 'school/resource/list.html'
    context_object_name = 'resources'


class ResourceDetailView(LoginRequiredMixin, DetailView):
    model = Resource
    template_name = 'school/resource/detail.html'


class ResourceCreateView(LoginRequiredMixin, CreateView):
    model = Resource
    template_name = 'school/resource/form.html'
    fields = ['title', 'description', 'file', 'subject']

    def form_valid(self, form):
        form.instance.uploaded_by = self.request.user.teacher
        return super().form_valid(form)



class SubjectListView(LoginRequiredMixin, ListView):
    model = Subject
    template_name = 'school/subjects/list.html'
    context_object_name = 'subjects'


class SubjectDetailView(LoginRequiredMixin, DetailView):
    model = Subject
    template_name = 'school/subjects/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subject = self.get_object()
        context['courses'] = Course.objects.filter()
        return context


# Home View
class HomePageView(TemplateView):
    template_name = 'school/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            if hasattr(self.request.user, 'student'):
                context['enrolled_courses'] = self.request.user.student.enrollments.all()
            elif hasattr(self.request.user, 'teacher'):
                context['teaching_courses'] = self.request.user.teacher.courses.all()
        context['total_students'] = Student.objects.count()
        context['total_teachers'] = Teacher.objects.count()
        context['total_courses'] = Course.objects.count()
        return context




# Student Views
class StudentListView(LoginRequiredMixin, ListView):
    model = Student
    template_name = 'school/student/list.html'
    context_object_name = 'students'
    ordering = ['grade', 'section']


class StudentDetailView(LoginRequiredMixin, DetailView):
    model = Student
    template_name = 'school/student/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = self.get_object()
        context['enrollments'] = student.enrollments.all()
        context['attendance'] = student.attendance_records.all()
        context['assignments'] = AssignmentSubmission.objects.filter(student=student)
        return context


class StudentCreateView(LoginRequiredMixin, CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'school/student/form.html'
    success_url = reverse_lazy('school:student-list')


# Teacher Views
class TeacherListView(LoginRequiredMixin, ListView):
    model = Teacher
    template_name = 'school/teacher/list.html'
    context_object_name = 'teachers'


class TeacherDetailView(LoginRequiredMixin, DetailView):
    model = Teacher
    template_name = 'school/teacher/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        teacher = self.get_object()
        context['courses'] = teacher.courses.all()
        return context


# Course Views
class CourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'school/courses/list.html'
    context_object_name = 'courses'


class CourseDetailView(LoginRequiredMixin, DetailView):
    model = Course
    template_name = 'school/courses/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_object()
        context['enrollments'] = course.enrollments.all()
        context['assignments'] = course.assignments.all()
        return context


# Attendance Views
def take_attendance(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        form = BulkAttendanceForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            present_students = form.cleaned_data['students']
            enrolled_students = Student.objects.filter(enrollments__course=course)

            for student in enrolled_students:
                Attendance.objects.create(
                    student=student,
                    course=course,
                    date=date,
                    is_present=student in present_students
                )
            messages.success(request, 'Attendance recorded successfully!')
            return redirect('school:course-detail', pk=course.id)
    else:
        form = BulkAttendanceForm(initial={'course': course})

    return render(request, 'school/attendance/take_attendance.html', {
        'form': form,
        'course': course
    })


# Assignment Views
class AssignmentCreateView(LoginRequiredMixin, CreateView):
    model = Assignment
    form_class = AssignmentForm
    template_name = 'school/assignment/form.html'

    def get_success_url(self):
        return reverse_lazy('school:course-detail', kwargs={'pk': self.object.course.id})


class AssignmentSubmissionCreateView(LoginRequiredMixin, CreateView):
    model = AssignmentSubmission
    form_class = AssignmentSubmissionForm
    template_name = 'school/assignment/submit.html'

    def get_success_url(self):
        return reverse_lazy('school:assignment-detail',
                            kwargs={'pk': self.object.assignment.id})


@login_required
def add_sermon(request):
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to add sermons.')
        return redirect('school:sermon_list')

    if request.method == 'POST':
        form = SermonForm(request.POST, request.FILES)
        if form.is_valid():
            sermon = form.save(commit=False)
            sermon.save()
            form.save_m2m()  # Save many-to-many relationships
            messages.success(request, 'Sermon added successfully!')
            return redirect('school:sermon_list', sermon_slug=sermon.slug)
    else:
        form = SermonForm()

    return render(request, 'school/sermons/add_sermon.html', {
        'form': form,
        'title': 'Add New Sermon'
    })