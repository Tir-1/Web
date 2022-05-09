from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, SubmitField, IntegerField, RadioField, EmailField, PasswordField, BooleanField, \
    TextAreaField
from wtforms.validators import DataRequired


class FindForm(FlaskForm):  # нахождение места по адресу
    name = StringField("Название: ", validators=[DataRequired()])
    z = IntegerField("Масштаб: ", validators=[DataRequired()], default=10)
    l = RadioField("Выбор формата", choices=["Карта", "Спутник", "Гибрид"], validators=[DataRequired()])
    submit = SubmitField("Подтвердить")


class CountForm(FlaskForm):  # вычисление расстояния
    name1 = StringField("Название: ", validators=[DataRequired()])
    name2 = StringField("Название: ", validators=[DataRequired()])
    submit = SubmitField("Подтвердить")


class RegisterForm(FlaskForm):  # форма регистрации
    email = EmailField('Почта', validators=[DataRequired()])
    name = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class AddTag(FlaskForm):  # Добваление метки
    name = StringField("Название метки: ", validators=[DataRequired()])
    address = StringField("Название места: ", validators=[DataRequired()])
    text = TextAreaField("Заметка: ", validators=[DataRequired()])
    public = BooleanField('Публичная запись')
    photo = FileField("Выберите фотографию", validators=[DataRequired()])
    submit = SubmitField("Подтвердить")


class AddDirect(FlaskForm):  # Добавление альбома
    name = StringField("Название директории: ", validators=[DataRequired()])
    submit = SubmitField("Подтвердить")
