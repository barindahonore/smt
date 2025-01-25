from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from .admin import admin_site

urlpatterns = [
    path('admin/', admin_site.urls),
    # path("admin/", admin.site.urls),
    path('', include('authentication.urls')),
    path('dashboard/', include('citizen.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('add/', include('admin_material.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
