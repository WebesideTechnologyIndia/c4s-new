from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # IMPORTANT: Custom admin routes PEHLE aani chahiye Django admin se
    path('', include('main_app.urls')),  # Ye pehle rakho
    path('admin/', admin.site.urls),     # Django admin baad mein
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)