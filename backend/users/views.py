from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import CreationForm
from flake8.api import legacy


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('reports:index')
    template_name = 'users/signup.html'

