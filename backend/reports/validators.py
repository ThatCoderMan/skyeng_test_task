from django import forms


def validate_py_file(value):
    if not value.name.endswith('.py'):
        raise forms.ValidationError(
            'Файл не соответвует формату (необходим .py)',
            params={'value': value},
        )
