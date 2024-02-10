import os
import aspose.pdf as ap
from django.urls import reverse
from django.conf import settings
from django.http import HttpResponse, FileResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile, UploadedFile
from .forms import SignupForm


def index(request):
    uploaded_files = UploadedFile.objects.all()
    return render(request, 'core/index.html', {'uploaded_files': uploaded_files})


def contact(request):
    return render(request, 'core/contact.html')


def profile(request):
    profile = Profile.objects.get(user=request.user)

    uploaded_files = UploadedFile.objects.filter(user=request.user)

    return render(request, 'core/profile.html', {'profile': profile, 'uploaded_files': uploaded_files})


def upload_latex_file(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['latex_file']
        if uploaded_file:
            if request.user.is_authenticated:
                user = request.user
            else:
                form = SignupForm()

                return render(request, 'core/signup.html', {
                    'form': form
                })

        uploaded_file_obj = UploadedFile(user=user, file=uploaded_file)
        uploaded_file_obj.save()

        file_path = os.path.join(settings.MEDIA_ROOT, uploaded_file.name)

        return render(request, 'core/upload_success.html', {'file_path': file_path})
    return render(request, 'core/upload.html')


def download_file(request, file_path):
    file_path = os.path.join(settings.MEDIA_ROOT, file_path)
    with open(file_path, 'rb') as file:
        response = HttpResponse(file.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
        return response


def download_pdf(request, file_path):
    original_file_path = os.path.join(settings.MEDIA_ROOT, file_path)
    options = ap.TeXLoadOptions()
    document = ap.Document(original_file_path, options)

    new_file_path = os.path.join(settings.MEDIA_ROOT, "newfile.pdf")
    document.save(new_file_path)

    with open(new_file_path, 'rb') as file:
        response = HttpResponse(file.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="newfile.pdf"'
        return response


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('/login/')
    else:
        form = SignupForm()

    return render(request, 'core/signup.html', {
        'form': form
    })

def file_details(request, file_id):
    file_obj = get_object_or_404(UploadedFile, pk=file_id)
    return render(request, 'core/file_details.html', {'file': file_obj})
