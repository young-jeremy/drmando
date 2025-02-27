from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Assignment
from .forms import AssignmentForm


@login_required
def assignment_create(request):
    if not (request.user.is_staff or hasattr(request.user, 'teacher')):
        messages.error(request, "You don't have permission to create assignments.")
        return redirect('school:assignment-list')

    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            assignment = form.save(commit=False)
            if hasattr(request.user, 'teacher'):
                assignment.teacher = request.user.teacher
            assignment.save()
            form.save_m2m()  # Save many-to-many relationships
            messages.success(request, 'Assignment created successfully!')
            return redirect('school:assignment-detail', pk=assignment.pk)
    else:
        form = AssignmentForm(user=request.user)

    return render(request, 'school/assignment_form.html', {
        'form': form,
        'title': 'Create New Assignment'
    })