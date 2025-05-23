from django.contrib import admin
from django.urls import path
from core.views import index, contact, about, upload_latex_file, download_file, download_pdf, signup, profile
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from core.forms import LoginForm
from core import views

urlpatterns = [
    path('', index, name='index'),
    path('contact/', contact, name='contact'),
    path('about/', about, name='about'),
    path('upload/', upload_latex_file, name='upload'),
    path('download/<str:file_path>/', download_file, name='download_file'),
    path('download_pdf/<str:file_path>/', download_pdf, name='download_pdf'),
    path('signup/', signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html',authentication_form=LoginForm), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', profile, name='profile'),
    path('file/<int:file_id>/', views.file_details, name='file_detail'),
    path('update_file/<int:file_id>/', views.update_file, name='update_file'),
    path('search/', views.search_files, name='search_files'),
    path('file/<int:file_id>/add_comment/', views.add_comment, name='add_comment'),
    path('save_comment_mark/', views.save_comment_mark, name='save_comment_mark'),
    path('delete_file/<int:file_id>/', views.delete_file, name='delete_file'),
    path('view_pdf/<int:file_id>/', views.view_pdf, name='view_pdf'),
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)