from django.contrib import admin
from django.urls import path
from core.views import index, contact, upload_latex_file
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', index, name='index'),
    path('contact/', contact, name='contact'),
    path('upload/', upload_latex_file, name='upload'),
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)