from functools import wraps
from http import HTTPStatus

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from .models import File


def check_is_owner(func):
    @wraps(func)
    def wrapper(request, pk, *args, **kwargs):
        user = get_object_or_404(File, pk=pk).user
        if user != request.user:
            return HttpResponseRedirect('/', HTTPStatus.FORBIDDEN)
        return func(request, pk, *args, **kwargs)
    return wrapper
