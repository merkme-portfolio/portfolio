import re
from http import HTTPStatus

from flask import jsonify, request, url_for

from . import app
from .constants import REGEX_PATTERNS, INFO_MESSAGES, MAX_LINK_LENGHT
from .error_handlers import InvalidAPIUsageError
from .models import URLMap
from .utils import generate_random_string


@app.route('/api/id/', methods=['POST'])
def create_short_url_api():
    """Создает короткую ссылку через API."""
    data = request.get_json()

    if not data:
        raise InvalidAPIUsageError(INFO_MESSAGES.get('no_data'))

    original_url = data.get('url')
    custom_id = data.get('custom_id')

    if not original_url:
        raise InvalidAPIUsageError(INFO_MESSAGES.get('no_url'))

    if not custom_id:
        custom_id = generate_random_string()
        data['custom_id'] = custom_id
        while URLMap.is_exists(custom_id):
            custom_id = generate_random_string()
            data['custom_id'] = custom_id

    if custom_id and len(custom_id) > MAX_LINK_LENGHT:
        raise InvalidAPIUsageError(INFO_MESSAGES.get('incorrect_name'))

    if data['custom_id']:
        if not re.search(REGEX_PATTERNS['link_short_id'], data['custom_id']):
            raise InvalidAPIUsageError(
                INFO_MESSAGES.get('incorrect_name')
            )

    if URLMap.is_exists(custom_id):
        raise InvalidAPIUsageError(INFO_MESSAGES.get('already_exists'))

    urlmap = URLMap.from_dict(data)
    urlmap.save_to_db()

    full_url = url_for('index_view', _external=True)
    response_data = {
        'url': original_url,
        'short_link': f'{full_url}{custom_id}'
    }
    return jsonify(response_data), HTTPStatus.CREATED


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_original_url_api(short_id):
    """Возвращает оригинальную ссылку при запросе по short_id."""
    link = URLMap.query.filter_by(short=short_id).first()
    if link:
        original_url = link.original
        response_data = {'url': original_url}
        return jsonify(response_data), HTTPStatus.OK
    raise InvalidAPIUsageError(
        INFO_MESSAGES.get('not_found'), HTTPStatus.NOT_FOUND
    )
