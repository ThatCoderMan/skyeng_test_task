import os

from django.contrib.auth import get_user_model
from django.db import models

from backend.settings import MEDIA_ROOT

from .validators import validate_py_file

User = get_user_model()


class File(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='files',
        verbose_name='пользователь'
    )
    file = models.FileField(
        upload_to='uploads_reports/',
        validators=(validate_py_file,)
    )
    created_at = models.DateTimeField(auto_now=True)
    is_reported = models.BooleanField(default=False)
    is_checked = models.BooleanField(default=False)
    is_reloaded = models.BooleanField(default=False)

    @property
    def filename(self):
        return os.path.basename(self.file.name)


class Report(models.Model):
    file = models.OneToOneField(
        File,
        on_delete=models.CASCADE,
        related_name='report',
        verbose_name='файл'
    )
    report_file = models.FileField(upload_to='reports/', null=True)

    @property
    def filename(self):
        return os.path.basename(self.report_file.path)

    @property
    def report_path(self):
        path = MEDIA_ROOT / 'reports'
        path.mkdir(exist_ok=True)
        return path


class Pep8Warning(models.Model):
    report = models.ForeignKey(
        Report,
        on_delete=models.CASCADE,
        related_name='pep8_warnings',
        verbose_name='отчёт по pep8'
    )
    status_code = models.CharField(max_length=5, verbose_name='код статуса')
    line = models.IntegerField(verbose_name='строка')
    column = models.IntegerField(verbose_name='столбец')
    message = models.CharField(max_length=255, verbose_name='сообщение')
    code_line = models.CharField(max_length=510, verbose_name='строка кода')

    def __str__(self):
        return f'{self.status_code} col:{self.column} [{self.message}]'
