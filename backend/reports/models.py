from django.contrib.auth import get_user_model
from django.db import models
from .validators import validate_py_file
import os

User = get_user_model()


class File(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='files',
        verbose_name='пользователь'
    )
    file = models.FileField(upload_to='data/uploads_reports/', validators=(validate_py_file,))
    created_at = models.DateTimeField(auto_now=True)
    is_reported = models.BooleanField(default=False)
    is_checked = models.BooleanField(default=False)

    @property
    def filename(self):
        return os.path.basename(self.file.name)


class Report(models.Model):
    ...