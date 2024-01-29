import os
import aspose.pdf as ap

from django.conf import settings
from django.http import HttpResponse, FileResponse
from django.shortcuts import render, redirect
from .models import Profile
from .forms import SignupForm


def index(request):
    return render(request, 'core/index.html')

def contact(request):
    return render(request, 'core/contact.html')


def profile(request):
    profile = Profile.objects.get(user=request.user)
    print ("username:" + str(profile.username))
    print(profile.email)
    return render(request, 'core/profile.html', {'profile': profile})

def upload_latex_file(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['latex_file']
        file_path = os.path.join(settings.MEDIA_ROOT, uploaded_file.name)

        with open(file_path, 'wb') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

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