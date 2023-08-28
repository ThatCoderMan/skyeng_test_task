from celery import shared_task
from django.core.mail import EmailMessage

from backend.settings import EMAIL_SENT_TIMEOUT
from reports.models import File, Pep8Warning, Report

from .utils import check_pep8_files, generate_report


@shared_task(name="repeat_file_checker")
def repeat_file_checker():
    unchecked_files = File.objects.filter(is_checked=False)
    if unchecked_files:
        file_paths = [str(file.file.path) for file in unchecked_files]
        results = check_pep8_files(file_paths)
        for file, result in zip(unchecked_files, results):
            old_report = Report.objects.filter(file=file)
            if old_report.exists():
                old_report.delete()
            report = Report(file=file)
            report.save()
            _, warnings, _ = result
            for warning in warnings:
                status_code, line, column, message, code_line = warning
                Pep8Warning(
                    report=report,
                    status_code=status_code,
                    line=line,
                    column=column,
                    message=message,
                    code_line=code_line
                ).save()
            generate_report(file)
            file.is_checked = True
            file.save()
            send_report.apply_async((file.pk,), countdown=EMAIL_SENT_TIMEOUT)


@shared_task(name="send_report")
def send_report(file_id):
    file = File.objects.get(pk=file_id)
    warnings_count = file.report.pep8_warnings.count()
    if warnings_count:
        message = (
            f'Файл {file.filename} проверен.\n'
            f'Найдено замечаний: {warnings_count}.'
        )
    else:
        message = f'Файл {file.filename} проверен.\n Замечаний не найдено.'
    email = EmailMessage(
        f'Отчёт по файлу: {file.filename}',
        message,
        'pep8@checker.com',
        [file.user.email]
    )
    if warnings_count:
        email.attach_file(str(file.report.report_file.path))
    email.send()
    file.is_reported = True
    file.save()
