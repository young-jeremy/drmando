from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Assignment
from .forms import AssignmentForm


@login_required
def assignment_edit(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)

    # Check permissions
    if not (request.user.is_staff or
            (hasattr(request.user, 'teacher') and request.user.teacher == assignment.teacher)):
        messages.error(request, "You don't have permission to edit this assignment.")
        return redirect('school:assignment-detail', pk=pk)

    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES, instance=assignment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Assignment updated successfully!')
            return redirect('school:assignment-detail', pk=pk)
    else:
        form = AssignmentForm(instance=assignment)

    return render(request, 'school/assignment_form.html', {
        'form': form,
        'assignment': assignment,
        'title': 'Edit Assignment'
    })


@login_required
def toggle_assignment_status(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)

    if not (request.user.is_staff or
            (hasattr(request.user, 'teacher') and request.user.teacher == assignment.teacher)):
        messages.error(request, "You don't have permission to modify this assignment.")
        return redirect('school:assignment-detail', pk=pk)

    assignment.is_active = not assignment.is_active
    assignment.save()

    status = "activated" if assignment.is_active else "deactivated"
    messages.success(request, f'Assignment {status} successfully!')

    return redirect('school:assignment-detail', pk=pk)


@login_required
def delete_assignment_file(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)

    if not (request.user.is_staff or
            (hasattr(request.user, 'teacher') and request.user.teacher == assignment.teacher)):
        messages.error(request, "You don't have permission to modify this assignment.")
        return redirect('school:assignment-detail', pk=pk)

    if assignment.file_attachment:
        assignment.file_attachment.delete()
        messages.success(request, 'Assignment file removed successfully!')

    return redirect('school:assignment-edit', pk=pk)