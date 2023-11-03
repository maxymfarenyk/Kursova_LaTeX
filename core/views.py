import os

from django.conf import settings
from django.shortcuts import render
from pylatex import Document, Section, Subsection, Command

def index(request):
    return render(request, 'core/index.html')

def contact(request):
    return render(request, 'core/contact.html')

def upload_latex_file(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['latex_file']
        file_path = os.path.join(settings.MEDIA_ROOT, uploaded_file.name)

        with open(file_path, 'wb') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        return render(request, 'core/upload_success.html')
    return render(request, 'core/upload.html')

