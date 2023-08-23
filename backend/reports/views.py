from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm
from django.contrib.auth.decorators import login_required
from .models import File
from django.shortcuts import get_object_or_404
from flake8.api import legacy as flake8


@login_required
def index(request):
    files_list = File.objects.filter(user=request.user)
    context = {
        'files': files_list
    }
    return render(request, 'report/index.html', context)


def upload_file(request):
    form = UploadFileForm(request.POST, files=request.FILES)
    if form.is_valid():
        file = form.save(commit=False)
        file.user = request.user
        file.save()
        print(form)
        return HttpResponseRedirect("/")
    print(form.errors)
    return HttpResponseRedirect("/")


@login_required
def delete_file(request, pk):
    file = get_object_or_404(File, pk=pk)
    if file.user != request.user:
        return redirect('/')
    file.delete()
    return HttpResponseRedirect("/")


@login_required
def edit_file(request, pk):
    old_file = get_object_or_404(File, pk=pk)
    if old_file.user != request.user or old_file.is_checked:
        return redirect('/')
    form = UploadFileForm(request.POST, files=request.FILES)
    if form.is_valid():
        file = form.cleaned_data['file']
        old_file.file = file
        old_file.save()
        print(form)
        return HttpResponseRedirect("/")
    print(form.errors)
    return HttpResponseRedirect("/")
