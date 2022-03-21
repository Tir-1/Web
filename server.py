from flask import Flask, render_template, redirect
from findform import FindForm
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
from z import start
menu = [{"name":"Главная страница", 'url':"/"}, {"name":"Поиск места", 'url':"/find"}]
@app.route('/')
@app.route('/index')
def index():
    return render_template("main page.html", title="Главная страница", menu=menu)


@app.route('/find', methods=['GET', 'POST'])
def start_find():
    form = FindForm()
    if form.validate_on_submit():
        n = form.name._value()
        return redirect(f'/image/{n}')
    return render_template('find image.html', title='Авторизация', form=form, menu=menu)


@app.route('/image/<x>')
def start_image(x):
    return render_template("image.html", title="Результаты", menu=menu, res=start(x))


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
