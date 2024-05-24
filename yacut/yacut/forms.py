from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import InputRequired, Length, Optional

from .validators import custom_id_validator


class URLForm(FlaskForm):
    """
    Форма для генерации коротких ссылок.

    Поля:
        original_link: Обязательное поле для ввода полного URL-адреса.
        custom_id: Поле для ввода короткого имени ссылки.
                   Длина от 1 до 16 символов, только латиница и цифры.
     Валидаторы:
        - original_link:
            - Обязательное поле.
            - Допустимая длина от 1 до 200 символов.

        - custom_id:
            - Опциональное поле.
            - Допустимая длина от 1 до 16 символов.
            - Пользовательский валидатор `custom_id_validator` проверяет,
              что короткое имя состоит из латинских букв и цифр.
    """

    original_link = URLField(
        'Вставьте вашу ссылку',
        validators=(
            InputRequired(message='Обязательное поле'),
            Length(1, 200),
        )
    )

    custom_id = StringField(
        'Короткое имя ссылки',
        validators=(Length(1, 16), Optional(), custom_id_validator)
    )
    submit = SubmitField('Создать')
