import os
import shutil
import subprocess
import tarfile
import zipfile
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseForbidden
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


def extract_archive(archive_path, extract_to):
    if zipfile.is_zipfile(archive_path):
        with zipfile.ZipFile(archive_path, 'r') as archive:
            archive.extractall(path=extract_to)
    elif archive_path.endswith('.tar.gz') or archive_path.endswith('.tgz'):
        with tarfile.open(archive_path, 'r:gz') as archive:
            archive.extractall(path=extract_to)
    elif tarfile.is_tarfile(archive_path):
        with tarfile.open(archive_path, 'r') as archive:
            archive.extractall(path=extract_to)
    else:
        raise RuntimeError("Непідтримуваний формат архіву. Підтримуються лише ZIP, TAR та TAR.GZ файли.")



def compile_with_pdflatex(tex_file_path, output_dir):
    command = [
        'pdflatex',
        '-interaction=nonstopmode',
        '-output-directory', output_dir,
        tex_file_path
    ]
    try:
        # Перша компіляція
        subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=os.path.dirname(tex_file_path))
        # Друга компіляція (для посилань і перехресних посилань)
        subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=os.path.dirname(tex_file_path))
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Помилка під час виконання pdflatex: {e.stderr.decode('utf-8')}")



def download_pdf(request, file_path):
    original_file_path = os.path.join(settings.MEDIA_ROOT, file_path)
    file_name = os.path.basename(original_file_path)
    file_display_name = os.path.splitext(file_name)[0]

    # Перевірка, чи файл існує
    if not os.path.exists(original_file_path):
        raise Http404("Файл не знайдено.")

    # Директорія для збереження PDF
    output_dir = os.path.join(settings.MEDIA_ROOT, 'pdf_generated', file_display_name)
    os.makedirs(output_dir, exist_ok=True)

    pdf_files = [f for f in os.listdir(output_dir) if f.endswith(".pdf")]
    if pdf_files:
        pdf_file_path = os.path.join(output_dir, pdf_files[0])
        return download_generated_pdf(pdf_file_path, file_display_name)

    else:
        return generate_pdf(original_file_path, file_name, file_display_name, output_dir)


def generate_pdf(original_file_path, file_name, file_display_name, output_dir):

    # Тимчасова директорія для роботи з файлами
    temp_dir = os.path.join(settings.MEDIA_ROOT, 'temp', file_display_name)
    os.makedirs(temp_dir, exist_ok=True)

    try:
        if zipfile.is_zipfile(original_file_path) or original_file_path.endswith(
                '.tar.gz') or original_file_path.endswith('.tgz') or tarfile.is_tarfile(original_file_path):
            # Якщо це архів, розпакувати його
            extract_archive(original_file_path, temp_dir)
            # Знайти головний .tex файл
            tex_files = [f for f in os.listdir(temp_dir) if f.endswith('.tex')]
            if not tex_files:
                raise RuntimeError("В архіві відсутні .tex файли.")

            tex_file_path = os.path.join(temp_dir, tex_files[0])
        else:
            # Якщо це одиничний .tex файл
            tex_file_path = os.path.join(temp_dir, file_name)
            shutil.copy(original_file_path, tex_file_path)

        # Отримуємо тільки ім'я файлу без шляху (наприклад, main_arxiv.tex)
        tex_file_name = os.path.basename(tex_file_path)

        # Компіляція у PDF
        compile_with_pdflatex(tex_file_path, output_dir)

        # Знайти згенерований PDF
        pdf_file_path = os.path.join(output_dir, f"{os.path.splitext(tex_file_name)[0]}.pdf")

        return download_generated_pdf(pdf_file_path, file_display_name)

    finally:
        # Очистка тимчасових файлів
        shutil.rmtree(temp_dir, ignore_errors=True)

def download_generated_pdf(pdf_file_path, file_display_name):
    with open(pdf_file_path, 'rb') as pdf_file:
        response = HttpResponse(pdf_file.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{file_display_name}.pdf"'
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

import os

def delete_file(request, file_id):
    try:
        file_obj = UploadedFile.objects.get(pk=file_id)
    except UploadedFile.DoesNotExist:
        raise Http404("Файл не знайдено.")

    # Перевіряємо, чи є користувач автором файлу
    if file_obj.user != request.user:
        return HttpResponseForbidden("У вас немає прав для видалення цього файлу.")

    # Збереження шляху до файлу перед видаленням з бази даних
    file_path = file_obj.file.path

    # Видалення запису з бази даних
    file_obj.delete()

    # Видалення фізичного файлу
    if os.path.exists(file_path):
        os.remove(file_path)

    # Повернення користувача на головну сторінку після видалення
    return redirect('index')

