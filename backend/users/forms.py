from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
# from .models import
User = get_user_model()


class CreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email',)
