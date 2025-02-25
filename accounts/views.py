from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from .forms import UserRegistrationForm, CustomAuthenticationForm
from .models import User
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from school.models import Assignment, Resource, Course, Enrollment, AssignmentSubmission
from django.db.models import Q
from datetime import datetime
from .forms import *
from django.views.generic import TemplateView
from school.models import *


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = 'accounts/profile_edit.html'
    fields = ['bio', 'avatar', 'phone_number']  # adjust fields as needed
    success_url = reverse_lazy('accounts:profile')

    def get_object(self, queryset=None):
        # Return the profile of the current logged-in user
        return self.request.user.profile



@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile')
    else:
        form = ProfileEditForm(instance=request.user.profile)

    return render(request, 'accounts/profile_edit.html', {
        'form': form
    })




class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.user_type == 'student':
            context['enrollments'] = user.student.enrollments.all()
        else:
            context['courses'] = user.teacher.courses.all()
        return context


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if hasattr(user, 'student'):
            # Get student's enrolled courses
            enrollments = user.student.enrollments.filter(is_active=True)
            courses = [enrollment.course for enrollment in enrollments]

            # Get assignments for enrolled courses
            context['assignments'] = Assignment.objects.filter(
                course__in=courses,
                due_date__gte=datetime.now()
            ).order_by('due_date')

            # Get submitted assignments
            context['submitted_assignments'] = user.student.submissions.all()

            # Get resources for enrolled courses
            context['resources'] = Resource.objects.filter(
                Q(subject__course__in=courses) & Q(is_active=True)
            ).order_by('-upload_date')

            context['enrollments'] = enrollments
            context['courses'] = courses

        elif hasattr(user, 'teacher'):
            # Get teacher's courses
            courses = user.teacher.courses.filter(is_active=True)

            # Get assignments for teacher's courses
            context['assignments'] = Assignment.objects.filter(
                course__in=courses
            ).order_by('due_date')

            # Get resources uploaded by teacher
            context['resources'] = Resource.objects.filter(
                uploaded_by=user.teacher
            ).order_by('-upload_date')

            # Get recent submissions
            context['recent_submissions'] = AssignmentSubmission.objects.filter(
                assignment__course__in=courses
            ).order_by('-submitted_at')[:10]

            context['courses'] = courses

        return context




class UserRegistrationView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Registration successful. Please login.')
        return response


def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.get_full_name()}!')
            return redirect('accounts:dashboard')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('accounts:login')


@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html')