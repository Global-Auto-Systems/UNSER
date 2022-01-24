from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
	path('', include('public.urls')),
	path('users/', include('users.urls')),
	path('ministry/', include('ministry.urls')),
	path('schools/', include('school.urls')),
    path('control/', admin.site.urls),
]
if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)