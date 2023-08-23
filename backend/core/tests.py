from flake8.api import legacy as flake8
from contextlib import redirect_stdout
import sys
import contextlib
import os


def f():
    with contextlib.redirect_stdout(open(os.devnull, 'w')):
        style_guide = flake8.get_style_guide(output_file=None)
        report = style_guide.check_files(['/Users/artemii/PycharmProjects/skyeng_test_task/backend/data/uploads_reports/time_test.py'])
        return report._application.file_checker_manager.results


print(f())