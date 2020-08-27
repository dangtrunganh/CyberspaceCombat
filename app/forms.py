from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField


class BeginForm(FlaskForm):
    submit = SubmitField('Start')


class HomeForm(FlaskForm):
    content = TextAreaField('Nhập nội dung')
    # submit = SubmitField('Predict')


