from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class FindForm(FlaskForm):
    name = StringField("Название: ", validators=[DataRequired()])
    z = IntegerField("Масштаб: ", validators=[DataRequired()], default=10)
    submit = SubmitField("Подтвердить")
