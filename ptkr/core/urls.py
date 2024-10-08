
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('ptkr.urls', namespace='ptkr'))
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


# CUSTOM DJANGO ADMIN
admin.site.site_header = "Dashboard Admin"
admin.site.site_title = "WEBGIS PTKR"
admin.site.index_title = "Dashboard Admin"
