from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_current_year(value):
    """
    Валидатор для проверки года произведения.
    """
    current_year = timezone.now().year
    if value > current_year:
        raise ValidationError(
            f'Год, который вы указали ({value}) \n'
            f'не может быть больше текущего ({current_year}).'
        )
