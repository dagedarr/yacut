from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .utils import generate_unique_url, validate_custom_id


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original(short_id):
    model = URLMap.query.filter_by(short=short_id).first()
    if model is None:
        # Тут код ответа нужно указать явным образом
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return jsonify(model.to_dict), 200


@app.route('/api/id/', methods=['POST'])
def add_url_map():
    data = request.get_json()

    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage('\"url\" является обязательным полем!')

    validate_custom_id(data.get('custom_id'))

    new_model = URLMap(
        original=data.get('url'),
        short=generate_unique_url() if data.get('custom_id') is None else data.get('custom_id'),
    )
    db.session.add(new_model)
    db.session.commit()
    return jsonify(
        {'url': new_model.original, 'short_link': f'{request.url_root}{new_model.short}'}
    ), 201
