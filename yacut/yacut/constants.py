"""Файл с константами."""
import re

REGEX_PATTERNS = {
    'link_short_id': re.compile(r'^[a-zA-Z0-9]+$'),
}

MAX_LINK_LENGHT = 16

INFO_MESSAGES = {
    'already_exists': 'Предложенный вариант короткой ссылки уже существует.',
    'created': 'Ваша ссылка создана:',
    'no_data': 'Отсутствует тело запроса',
    'no_url': '"url" является обязательным полем!',
    'incorrect_name': 'Указано недопустимое имя для короткой ссылки',
    'not_found': 'Указанный id не найден'
}
