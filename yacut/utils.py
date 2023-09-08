import random
import re
import string

from flask import flash, request

from . import db
from .error_handlers import InvalidAPIUsage
from .models import URLMap


class Messages:
    REPEATED_URL = 'Имя {short_name} уже занято!'
    REPEATED_URL_2 = 'Имя "{short_name}" уже занято.'
    SUCCESS = 'Успешное создание ссылки'


def randomize_url():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(6))


def is_custom_url_exists(custom_url):
    """
    Проверяет, существует ли пользовательский URL в базе данных.
    """
    return URLMap.query.filter_by(short=custom_url).first() is not None


def generate_unique_url():
    """
    Генерирует уникальный пользовательский URL.
    """
    custom_url = randomize_url()
    # `randomize_url()` вывел повторяющийся `custom_url`
    while is_custom_url_exists(custom_url):
        custom_url = randomize_url()
    return custom_url


def create_new_url_map(original_link, short_url):
    """
    Создает новую запись URLMap в базе данных.
    """
    new_model = URLMap(
        original=original_link,
        short=short_url,
    )
    db.session.add(new_model)
    db.session.commit()
    return new_model


def flash_repeated_url_message(custom_url):
    """
    Выводит сообщение о том, что пользовательский URL уже существует.
    """
    flash(Messages.REPEATED_URL.format(short_name=custom_url))


def flash_success_message(short_url):
    """
    Выводит сообщение об успешном создании и короткой ссылке.
    """
    flash(Messages.SUCCESS)
    flash(f'{request.url_root}{short_url}')


def does_short_url_correct(url):
    pattern = re.compile(r'^[A-Za-z0-9]+$')
    return bool(pattern.match(url))


def validate_custom_id(custom_id):
    if (custom_id and len(custom_id) > 16) or (custom_id and not does_short_url_correct(custom_id)):
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
    if URLMap.query.filter_by(short=custom_id).first() is not None:
        raise InvalidAPIUsage(Messages.REPEATED_URL_2.format(short_name=custom_id))
