from django.conf import settings
from django.contrib.auth.tokens import default_token_generator


def generate_confirmation_code(user):
    """Генерирует и сохраняет код подтверждения для пользователя."""
    confirmation_code = default_token_generator.make_token(user)
    user.confirmation_code = confirmation_code
    user.save()
    return confirmation_code


def send_confirmation_email(user, confirmation_code):
    """Отправляет письмо с кодом подтверждения пользователю."""
    subject = f'Код подтверждения для {user.username}'
    message = f'Ваш код подтверждения {confirmation_code}'
    from_email = settings.ADMIN_EMAIL
    user.email_user(subject, message, from_email)


def check_confirmation_code(user, confirmation_code):
    """Проверяет предоставленный код подтверждения."""
    return default_token_generator.check_token(user, confirmation_code)
