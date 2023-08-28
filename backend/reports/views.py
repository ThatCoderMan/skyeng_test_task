from http import HTTPStatus

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import FileResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render

from backend.settings import ITEMS_ON_PAGE

from .forms import UploadFileForm
from .models import File
from .permissions import check_is_owner


@login_required
def index(request):
    files_list = File.objects.filter(
        user=request.user
    ).select_related('user').prefetch_related('report').order_by('-created_at')
    paginator = Paginator(files_list, ITEMS_ON_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj
    }
    return render(request, 'report/index.html', context)


def upload_file(request):
    form = UploadFileForm(request.POST, files=request.FILES)
    if form.is_valid():
        file = form.save(commit=False)
        file.user = request.user
        file.save()
        return HttpResponseRedirect('/', HTTPStatus.NO_CONTENT)
    for error in form.errors.values():
        messages.error(request, error[0])
    return HttpResponseRedirect('/', HTTPStatus.INTERNAL_SERVER_ERROR)


@login_required
@check_is_owner
def delete_file(request, pk):
    file = get_object_or_404(File, pk=pk)
    file.delete()
    return HttpResponseRedirect('/', HTTPStatus.NO_CONTENT)


@login_required
@check_is_owner
def edit_file(request, pk):
    file = get_object_or_404(File, pk=pk)
    form = UploadFileForm(request.POST, files=request.FILES)
    if form.is_valid():
        new_file = form.cleaned_data['file']
        file.file = new_file
        file.is_reloaded = True
        file.is_reported = False
        file.is_checked = False
        file.save()
        return HttpResponseRedirect('/', HTTPStatus.NO_CONTENT)
    for error in form.errors.values():
        messages.error(request, error[0])
    return HttpResponseRedirect('/', HTTPStatus.INTERNAL_SERVER_ERROR)


@login_required
@check_is_owner
def get_file(request, pk):
    file = get_object_or_404(File, pk=pk)
    return FileResponse(file.file, 'rb')


@login_required
@check_is_owner
def get_report(request, pk):
    file = get_object_or_404(File, pk=pk)
    report = file.report
    return FileResponse(report.report_file, 'rb')
