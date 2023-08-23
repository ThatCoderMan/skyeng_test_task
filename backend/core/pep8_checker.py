from flake8.api import legacy as flake8
from contextlib import redirect_stdout
import os


def check_pep8_files(paths: list[str]):
    with redirect_stdout(open(os.devnull, 'w')):
        style_guide = flake8.get_style_guide(output_file=None)
        report = style_guide.check_files(paths)
        return report._application.file_checker_manager.results
