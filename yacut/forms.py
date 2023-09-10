from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp

from .utils import Constants


class URLForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[DataRequired(message='Обязательное поле'), Length(1, 128)]
    )
    custom_id = URLField(
        'Ваш вариант короткой ссылки',
        validators=[Optional(),
                    Length(max=Constants.MAX_URL_LENGHT),
                    Regexp(Constants.REGEXP, message='Некорректный формат')
                    ]
    )

    submit = SubmitField('Добавить')