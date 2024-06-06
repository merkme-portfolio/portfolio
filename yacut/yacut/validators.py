from wtforms.validators import Regexp

from .constants import REGEX_PATTERNS

custom_id_validator = Regexp(
    regex=REGEX_PATTERNS['link_short_id'],
    message=(
        'Недопустимый формат короткого id. '
        'Допустимы только латинские буквы и цифры.'
    )
)
