from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Assignment


@login_required
def assignment_delete(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)

    if not (request.user.is_staff or
            (hasattr(request.user, 'teacher') and request.user.teacher == assignment.teacher)):
        messages.error(request, "You don't have permission to delete this assignment.")
        return redirect('school:assignment-detail', pk=pk)

    if request.method == 'POST':
        assignment.delete()
        messages.success(request, 'Assignment deleted successfully!')
        return redirect('school:assignment-list')

    return render(request, 'school/assignment_delete.html', {
        'assignment': assignment
    })