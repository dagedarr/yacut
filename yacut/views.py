from flask import abort, redirect, render_template, request

from . import app
from .forms import URLForm
from .models import URLMap
from .utils import (create_new_url_map, flash_repeated_url_message,
                    flash_success_message, generate_unique_url,
                    is_custom_url_exists)


@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Отображает главную страницу и обрабатывает запросы на создание новой короткой ссылки.
    """
    form = URLForm()

    if request.method == 'POST' and form.validate_on_submit():
        custom_url = form.custom_id.data
        # Пользователь ввел повторяющийся `custom_url`
        if custom_url and is_custom_url_exists(custom_url):
            flash_repeated_url_message(custom_url)
            return render_template('index.html', form=form)

        if not custom_url:
            custom_url = generate_unique_url()

        new_model = create_new_url_map(
            original_link=form.original_link.data,
            short_url=custom_url
        )
        flash_success_message(new_model.short)

    return render_template('index.html', form=form)


@app.route('/<string:short_url>')
def opinion_view(short_url):
    """
    Отображает оригинальную ссылку на основе короткого URL.
    """
    db_url = URLMap.query.filter_by(short=short_url).first()
    if not db_url:
        abort(404)
    return redirect(db_url.original)