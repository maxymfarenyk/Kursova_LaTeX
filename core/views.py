import os
import aspose.pdf as ap
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile, UploadedFile, Comment
from .forms import SignupForm
from django.db.models import Subquery, OuterRef
import re
from .forms import CommentForm

def index(request):
    latest_files = UploadedFile.objects.filter(
        version=Subquery(
            UploadedFile.objects.filter(display_name=OuterRef('display_name')).order_by('-version').values('version')[
            :1]
        )
    ).order_by('-upload_date')


    return render(request, 'core/index.html', {'latest_files': latest_files})

def contact(request):
    return render(request, 'core/contact.html')

def about(request):
    return render(request, 'core/about.html')

def profile(request):
    profile = Profile.objects.get(user=request.user)
    uploaded_files = UploadedFile.objects.filter(
        version=Subquery(
            UploadedFile.objects.filter(display_name=OuterRef('display_name')).order_by('-version').values('version')[
            :1]
        ),
        user=request.user
    ).order_by('-upload_date')
    return render(request, 'core/profile.html', {'profile': profile, 'uploaded_files': uploaded_files})



def upload_latex_file(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['latex_file']
        if uploaded_file:
            if request.user.is_authenticated:
                user = request.user
            else:
                form = SignupForm()
                return render(request, 'core/signup.html', {'form': form})

        file_name = os.path.basename(uploaded_file.name)
        safe_file_name = re.sub(r'\s+', '_', file_name)
        safe_file_name = re.sub(r'[(){}[\]<>]', '', safe_file_name)
        uploaded_file_obj = UploadedFile(user=user, file=uploaded_file, display_name=safe_file_name)
        uploaded_file_obj.save()

        return render(request, 'core/upload_success.html', {'file_path': safe_file_name})
    return render(request, 'core/upload.html')


def update_file(request, file_id):
    if request.method == 'POST':
        uploaded_file = request.FILES['updated_file']
        if uploaded_file:
            user = request.user

            existing_file = UploadedFile.objects.get(pk=file_id)

            new_version = existing_file.version + 1

            updated_file_obj = UploadedFile(user=user, file=uploaded_file, display_name=existing_file.display_name, version=new_version)
            updated_file_obj.save()

            return redirect('index')
    else:
        existing_file = UploadedFile.objects.get(pk=file_id)
        return render(request, 'core/update_file.html', {'existing_file': existing_file})

def download_file(request, file_path):
    file_path = os.path.join(settings.MEDIA_ROOT, file_path)
    with open(file_path, 'rb') as file:
        response = HttpResponse(file.read())
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
        return response


def download_pdf(request, file_path):
    original_file_path = os.path.join(settings.MEDIA_ROOT, file_path)
    file_name = os.path.basename(original_file_path)
    file_display_name = os.path.splitext(file_name)[0]

    options = ap.TeXLoadOptions()
    document = ap.Document(original_file_path, options)
    uploaded_file = UploadedFile.objects.get(file=file_path)
    file_version = uploaded_file.version
    new_file_path = os.path.join(settings.MEDIA_ROOT, f"{file_display_name}_v{file_version}.pdf")
    document.save(new_file_path)

    with open(new_file_path, 'rb') as file:
        response = HttpResponse(file.read())
        response['Content-Disposition'] = f'attachment; filename="{file_display_name}_v{file_version}.pdf"'
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
    all_versions = UploadedFile.objects.filter(display_name=file_obj.display_name).order_by('-version')

    comments = Comment.objects.filter(file=file_obj).order_by('-created_at')

    comment_form = CommentForm()

    return render(request, 'core/file_details.html',
                  {'file': file_obj, 'all_versions': all_versions, 'comment_form': comment_form, 'comments': comments})


def add_comment(request, file_id):
    file_obj = get_object_or_404(UploadedFile, pk=file_id)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.file = file_obj
            comment.save()
            return redirect('file_detail', file_id=file_id)

    return redirect('file_detail', file_id=file_id)
def save_comment_mark(request):
    if request.method == 'POST':
        comment_id = request.POST.get('comment_id')
        mark = request.POST.get('mark')

        comment = Comment.objects.filter(id=comment_id, file__user=request.user).first()
        if comment:
            comment.mark = mark
            comment.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def search_files(request):
    query = request.GET.get('query')
    if query:
        latest_files = UploadedFile.objects.filter(
            display_name__icontains=query,
            version=Subquery(
                UploadedFile.objects.filter(display_name=OuterRef('display_name')).order_by('-version').values('version')[:1]
            )
        )
    else:
        latest_files = []
    return render(request, 'core/search_results.html', {'found_files': latest_files, 'query': query})


