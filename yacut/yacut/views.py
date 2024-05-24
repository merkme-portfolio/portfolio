from flask import flash, redirect, render_template, url_for

from . import app
from .forms import URLForm
from .models import URLMap
from .utils import generate_random_string
from .constants import INFO_MESSAGES
from .enums.message_types import FlashTypes


@app.route('/', methods=['GET', 'POST'])
def index_view():
    """
    Главная страница. Реализована генирация коротких ссылок.

    Форма, содержащая данные оригинальной и, возможно,
    пользовательской короткой ссылки.

    Если не указать короткую ссылку, то она будет сгенерирована автоматически.
    """
    form = URLForm()
    if form.validate_on_submit():
        custom_id = form.custom_id.data

        if not custom_id:
            custom_id = generate_random_string()
            while URLMap.is_exists(custom_id):
                custom_id = generate_random_string()

        if URLMap.is_exists(custom_id):
            flash(
                INFO_MESSAGES.get('already_exists'),
                FlashTypes.ERROR.value
            )
            return render_template('urlmap.html', form=form)

        new_mapping = URLMap(
            original=form.original_link.data,
            short=custom_id
        )

        new_mapping.save_to_db()

        full_url = url_for('index_view', _external=True)
        flash(INFO_MESSAGES.get('created'), FlashTypes.INFO.value)
        flash(f'{full_url}{new_mapping.short}', FlashTypes.LINK.value)

    return render_template('urlmap.html', form=form)


@app.route('/<short_id>')
def redirect_to_original(short_id):
    """Функция которая отвечает за редирект пользователя по короткой ссылке."""
    url_mapping = URLMap.query.filter_by(short=short_id).first_or_404()
    return redirect(url_mapping.original)
