from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, HttpResponseNotFound
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Assignment


@login_required
def assignment_list(request):
    # Get filters from request
    subject = request.GET.get('subject')
    priority = request.GET.get('priority')
    status = request.GET.get('status')
    search_query = request.GET.get('search', '').strip()

    # Start with all assignments
    assignments = Assignment.objects.all()

    # Apply filters based on user type
    if hasattr(request.user, 'student'):
        assignments = assignments.filter(
            grade_level=request.user.student.grade_level,
            is_active=True
        )
    elif hasattr(request.user, 'teacher'):
        assignments = assignments.filter(teacher=request.user.teacher)
    elif not request.user.is_staff:
        assignments = Assignment.objects.none()

    # Apply search filter
    if search_query:
        assignments = assignments.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(subject__name__icontains=search_query)
        )

    # Apply other filters
    if subject:
        assignments = assignments.filter(subject_id=subject)
    if priority:
        assignments = assignments.filter(priority=priority)
    if status:
        if status == 'active':
            assignments = assignments.filter(is_active=True)
        elif status == 'inactive':
            assignments = assignments.filter(is_active=False)

    # Pagination
    paginator = Paginator(assignments, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'priorities': Assignment.PRIORITY_CHOICES,
        'courses': request.user.teacher.subjects.all() if hasattr(request.user, 'teacher') else None,
        # Changed from subjects
        'current_subject': subject,
        'current_priority': priority,
        'current_status': status,
        'search_query': search_query,
    }

    return render(request, 'school/assignments/assignment_list.html', context)


@login_required
def assignment_detail(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)

    # Check if user has access to this assignment
    if not (request.user.is_staff or
            (hasattr(request.user, 'teacher') and request.user.teacher == assignment.teacher) or
            (hasattr(request.user, 'student') and request.user.student.grade_level == assignment.grade_level)):
        messages.error(request, "You don't have permission to view this assignment.")
        return redirect('school:assignment-list')

    context = {
        'assignment': assignment,
    }
    return render(request, 'school/assignments/assignment_detail.html', context)


@login_required
def download_assignment_file(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    if assignment.file_attachment:
        return FileResponse(assignment.file_attachment.open(), as_attachment=True)
    return HttpResponseNotFound('File not found')