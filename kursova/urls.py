from django.contrib import admin
from django.urls import path
from core.views import index, contact, upload_latex_file, download_file, download_pdf, signup
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from core.forms import LoginForm

urlpatterns = [
    path('', index, name='index'),
    path('contact/', contact, name='contact'),
    path('upload/', upload_latex_file, name='upload'),
    path('download/<str:file_path>/', download_file, name='download_file'),
    path('download_pdf/<str:file_path>/', download_pdf, name='download_pdf'),
    path('signup/', signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html',authentication_form=LoginForm), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)