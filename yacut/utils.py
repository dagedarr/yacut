import random
import re
import string

from flask import flash, request

from . import db
from .error_handlers import InvalidAPIUsage


class Messages:
    REPEATED_URL = 'Имя {short_name} уже занято!'
    REPEATED_URL_2 = 'Имя "{short_name}" уже занято.'
    SUCCESS = 'Успешное создание ссылки'
    INCORRECT_NAME = 'Указано недопустимое имя для короткой ссылки'


class Constants:
    REGEXP = r'^[A-Za-z0-9]+$'
    MAX_URL_LENGHT = 16


def randomize_url():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(6))


def is_custom_url_exists(custom_url, model):
    """
    Проверяет, существует ли пользовательский URL в базе данных.
    """
    return model.query.filter_by(short=custom_url).first() is not None


def generate_unique_url(model):
    """
    Генерирует уникальный пользовательский URL.
    """
    custom_url = randomize_url()
    # `randomize_url()` вывел повторяющийся `custom_url`
    while is_custom_url_exists(custom_url, model):
        custom_url = randomize_url()
    return custom_url


def create_new_url_map(original_link, short_url, model):
    """
    Создает новую запись модели (URLMap) в базе данных.
    """
    new_model = model(
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
    """
    Проверяет корректность короткой ссылки.
    """
    pattern = re.compile(Constants.REGEXP)
    return bool(pattern.match(url))


def validate_custom_id(custom_id, model):
    """
    Проверяет корректность короткой ссылки для добавления в БД.
    """
    if custom_id and (len(custom_id) > Constants.MAX_URL_LENGHT or not does_short_url_correct(custom_id)):
        raise InvalidAPIUsage(Messages.INCORRECT_NAME)
    if model.query.filter_by(short=custom_id).first() is not None:
        raise InvalidAPIUsage(Messages.REPEATED_URL_2.format(short_name=custom_id))
