from django.contrib import admin

from .models import File, Pep8Warning, Report


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'filename',
        'created_at',
        'is_reported',
        'is_checked'
    )


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('file', 'report_file')


@admin.register(Pep8Warning)
class Pep8WarningAdmin(admin.ModelAdmin):
    list_display = (
        'report',
        'status_code',
        'line',
        'column',
        'message',
        'code_line'
    )
