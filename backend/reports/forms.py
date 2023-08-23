from django import forms
from .models import File
from django.contrib.auth import get_user_model

User = get_user_model()


class UploadFileForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.all(), required=False)

    class Meta:
        model = File
        fields = ('file', 'user')


