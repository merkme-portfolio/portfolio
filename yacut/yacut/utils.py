import random
import string


def generate_random_string(length=6):
    """Генерация случайной строки состоящей из 6 символов."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))
