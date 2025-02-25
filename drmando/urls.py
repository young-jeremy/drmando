from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('school.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    # path('api/', include('school.api.urls')),  # If you want to add API endpoints
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)