from django.urls import path
from . import views
from .views import subject_edit

app_name = 'school'

urlpatterns = [


    path('', views.video_list, name='video_list'),
    path('videos/<int:video_id>/', views.video_detail, name='video_detail'),
    path('videos/upload/', views.upload_video, name='upload_video'),
    path('videos/<int:video_id>/edit/', views.edit_video, name='edit_video'),
    path('videos/<int:video_id>/like/', views.like_video, name='like_video'),




    # Home URL
    path('home/', views.HomePageView.as_view(), name='home'),

    # Student URLs
    path('students/', views.StudentListView.as_view(), name='student-list'),
    path('students/add/', views.StudentCreateView.as_view(), name='student-create'),
    path('students/<int:pk>/', views.StudentDetailView.as_view(), name='student-detail'),

    # Teacher URLs
    path('teachers/', views.TeacherListView.as_view(), name='teacher-list'),
    path('teachers/<int:pk>/', views.TeacherDetailView.as_view(), name='teacher-detail'),

    # Course URLs
    path('courses/', views.CourseListView.as_view(), name='course_list'),
    path('courses/<int:pk>/', views.CourseDetailView.as_view(), name='course_detail'),
    path('create/', views.create_course, name='create_course'),

    # Attendance URLs
    path('courses/<int:course_id>/attendance/', views.take_attendance, name='take-attendance'),

    # Assignment URLs
    path('assignments/create/', views.AssignmentCreateView.as_view(), name='assignment-create'),
    path('assignments/<int:pk>/submit/', views.AssignmentSubmissionCreateView.as_view(), name='assignment-submit'),

# Subject URLs (new)
    path('subjects/', views.SubjectListView.as_view(), name='subject-list'),
    path('subjects/<int:pk>/', views.SubjectDetailView.as_view(), name='subject-detail'),

    # Resource URLs
    path('resources/', views.ResourceListView.as_view(), name='resource-list'),
    path('resources/<int:pk>/', views.ResourceDetailView.as_view(), name='resource-detail'),
    path('resources/create/', views.ResourceCreateView.as_view(), name='resource-create'),

    # About URL
    path('about/', views.AboutView.as_view(), name='about'),
    # Add to your existing URLs
    path('contact/', views.ContactView.as_view(), name='contact'),

    path('privacy/', views.PrivacyView.as_view(), name='privacy'),

    # Sermon URLs
    path('sermons/', views.sermon_list, name='sermon_list'),
    path('sermons/<slug:sermon_slug>/', views.sermon_detail, name='sermon_details'),  # Fixed duplicate slug
    path('sermons/<slug:sermon_slug>/like/', views.like_sermon, name='like_sermon'),
    path('sermons/<slug:sermon_slug>/note/', views.save_note, name='save_note'),
    path('sermons/add/', views.add_sermon, name='add_sermon'),
    # Category URLs
    path('categories/', views.sermon_categories, name='categories'),
    path('categories/<slug:category_slug>/edit/', views.edit_sermon_category, name='edit_category'),
    path('categories/<slug:category_slug>/delete/', views.delete_sermon_category, name='delete_category'),


    path('subjects/create/', views.subject_create, name='subject-create'),
    path('subjects/<int:pk>/edit/', views.subject_edit, name='subject-edit'),
    path('subjects/<int:pk>/delete/', views.subject_delete, name='subject-delete'),
    path('subjects/<int:pk>/toggle-status/', views.subject_toggle_status, name='subject-toggle-status'),


    # ... other URLs ...
    path('subjects/<int:pk>/edit/', views.subject_edit, name='subject-edit'),
    path('subjects/<int:pk>/toggle-status/', views.subject_toggle_status, name='subject-toggle-status'),
    path('subjects/<int:pk>/delete-file/<str:file_type>/', views.subject_delete_file, name='subject-delete-file'),




]