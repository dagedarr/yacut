from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField
from wtforms.validators import DataRequired, Length


class URLForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[DataRequired(message='Обязательное поле'),
                    Length(1, 128)]
    )
    custom_id = URLField(
        'Ваш вариант короткой ссылки',
        validators=[Length(max=16)]
    )

    submit = SubmitField('Добавить')