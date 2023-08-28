import os
from contextlib import redirect_stdout

from flake8.api import legacy as flake8
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate


def generate_report(file):
    file_path = file.file.path
    file_name = file.filename
    report = file.report
    output_file = str(
        report.report_path / file_name.replace('.py', '.pdf')
    )

    with open(file_path, 'r') as source_file:
        source_code = source_file.read().split('\n')

    elements = []
    style_sheet = getSampleStyleSheet()
    code_style = style_sheet['Code']
    header = style_sheet['Title']

    elements.append(Paragraph(f'Report: {file_name}', header))

    for code_line, code in enumerate(source_code, start=1):
        code_text = f'{code_line}. {code}'
        warnings = report.pep8_warnings.filter(line=code_line)
        if warnings:
            warnings_text = "<br/>".join(map(str, warnings))
            code_text += f'<br/><font color="red">{warnings_text}</font>'
        code_paragraph = Paragraph(code_text, code_style)
        elements.append(code_paragraph)

    warnings_count = report.pep8_warnings.count()
    total_warnings = (
        f'<br/><font color="red">Total warnings: {warnings_count}</font>'
    )
    code_paragraph = Paragraph(total_warnings, code_style)
    elements.append(code_paragraph)

    doc = SimpleDocTemplate(
        output_file,
        pagesize=letter,
        leftMargin=10,
        rightMargin=10,
        topMargin=30,
        bottomMargin=30
    )
    doc.build(elements)
    report.report_file = output_file
    report.save()


def check_pep8_files(paths: list[str]) -> list[str, list[5], dict]:
    with redirect_stdout(open(os.devnull, 'w')):
        style_guide = flake8.get_style_guide(output_file=None)
        report = style_guide.check_files(paths)
        return report._application.file_checker_manager.results
