from flask import Flask, render_template, redirect
from findform import FindForm, FindForm2, CountForm, LoginForm, AddTag, AddDirect
from create.create_map import start
from create.count_S import coordinates
from data import db_session
from findform import RegisterForm
from data.users import User
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from create.test import load_map
from create.main import get_coord
from data.tags import Tags_of_map
from data.directories import Directory
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
menu = [{"name": "Главная страница", 'url': "/"}, {"name": "Поиск места", 'url': "/find"},
        {"name": "Вычисление расстояния", 'url': "/S"}, {"name": "Дневник путешествиника", 'url': "/blog/-1"}]
login_manager = LoginManager()
login_manager.init_app(app)
n1 = 0
default1 = ""
@app.route('/')
@app.route('/index')
def index():
    return render_template("main page.html", title="Главная страница", menu=menu)
@app.route('/find', methods=['GET', 'POST'])
def start_find():
    form = FindForm()
    if form.validate_on_submit():
        n = str(form.name._value()) + ";" + str(form.z._value()) + ";" + str(form.l.data)
        return redirect(f'/image/{n}')
    return render_template('find image.html', title='Поиск места', form=form, menu=menu)
@app.route('/S', methods=['GET', 'POST'])
def count():
    form = CountForm()
    if form.validate_on_submit():
        n = str(form.name1._value() + ";" + form.name2._value())
        return redirect(f'/count/{coordinates(n)}')
    return render_template('count.html', title='Поиск места', form=form, menu=menu)
@app.route('/find2', methods=['GET', 'POST'])
def start_find2():
    form = FindForm2()
    if form.validate_on_submit():
        n = str(form.name._value())
        return redirect(f'/image/{n}')
    return render_template('find image.html', title='Авторизация', form=form, menu=menu)
@app.route('/image/<x>')
def start_image(x,check=0):
    global n1
    n1 = x
    return render_template("image.html", title="Результаты", menu=menu, res=start(x, check), image=f"/static/{current_user.name}.png")
@app.route('/count/<x>')
def start7(x):
    return render_template("count_res.html", text=x)
@app.route("/register", methods=['GET', 'POST'])
def registration():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('registr.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('registr.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('registr.html', title='Регистрация', form=form, menu=menu)
@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('log.html',
                               message="Неправильный логин или пароль",
                               form=form, menu=menu)
    return render_template('log.html', title='Авторизация', form=form, menu=menu)
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")
@app.route("/blog/<tag>")
def blog(tag):
    if current_user.is_authenticated:
        info = []
        text, name, location = "", "", ""
        db_sess = db_session.create_session()
        for i in db_sess.query(Tags_of_map).filter(Tags_of_map.user_id == current_user.id):
            i.color = "pmwtm"
            db_sess.commit()
        if tag[:4] == "dir_":
            direct = db_sess.query(Directory).filter(Directory.id == tag[4:]).first()
            check = direct.tags
            check = check.split(";")
            info.append({"name": "Назад", "id": "", "url": "/blog/-1"})
            for i in db_sess.query(Tags_of_map).filter(Tags_of_map.user_id == current_user.id,
                                                       Tags_of_map.id.in_(check)):
                d = {"name": i.name, "id": i.id, "url": "/blog/" + str(i.id)}
                info.append(d)
        elif tag != "-1":
            n = db_sess.query(Tags_of_map).filter(Tags_of_map.user_id == current_user.id, Tags_of_map.id == tag).first()
            n.color = "pmrdm"
            text = n.description
            name = n.name
            location = n.location
            db_sess.commit()
            info = [{"name": "Назад", "id": "", "url": "/blog/-1"},
                    {"name": "Удалить эту запись", "id": "", "url": f"/delete/{tag}"}]
            if n.in_directory == 0:
                info.append({"name": "Добавить эту метку в альбом", "id": "", "url": f"/add_to_dir/{tag}"})
            else:
                info.append({"name": "Перенести запись", "id": "", "url": f"/add_to_dir/{tag}"})
        else:
            for i in db_sess.query(Tags_of_map).filter(Tags_of_map.user_id == current_user.id, Tags_of_map.in_directory == 0):
                d = {"name": i.name, "id": i.id, "url": "/blog/" + str(i.id)}
                info.append(d)
            for i in db_sess.query(Directory).filter(Directory.user_id == current_user.id):
                d = {"name": i.name, "id": i.id, "url": "/blog/dir_" + str(i.id)}
                info.append(d)
        load_map()
        menu2 = menu + [{"name": "Новая метка", 'url': "/add"}, {"name": "Создать новый альбом", 'url': "/direct"}]
        return render_template('my_blog.html', title='Блог', menu=menu2, tag_list=info,
                               tag=tag[3:], text=text, name=name,
                               location=location, image=f"/static/{current_user.name}.png")
    else:
        return "Пока"
@app.route("/add", methods=['GET', 'POST'])
def add():
    form = AddTag()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        tag = Tags_of_map()
        tag.location = form.address._value()
        tag.coord = get_coord(form.address._value())
        tag.name = form.name._value()
        tag.description = form.text._value()
        tag.user_id = current_user.id
        tag.in_directory = 0
        current_user.tags.append(tag)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect("blog/-1")
    return render_template("addtag.html", title="Добавление метки", form=form)
@app.route("/delete/<tag>", methods=['GET', 'POST'])
def delete(tag):
    db_sess = db_session.create_session()
    db_sess.query(Tags_of_map).filter(Tags_of_map.id == tag).delete()
    db_sess.commit()
    return redirect("/blog/-1")
@app.route("/direct", methods=['GET', 'POST'])
def create():
    form = AddDirect()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        new = Directory()
        new.name = form.name._value()
        new.user_id = current_user.id
        new.tags = ""
        current_user.directories.append(new)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect("blog/-1")
    return render_template("addtag.html", title="Добавление директории", form=form)
@app.route("/add_to_dir/<num>")
def cr2(num):
    db_sess = db_session.create_session()
    text = [{"name": "Назад", "id": "/blog/-1"}]
    tg = db_sess.query(Tags_of_map).filter(Tags_of_map.id == num).first()
    if tg.in_directory == 0:
        title = "Ваши директории"
        for i in db_sess.query(Directory).filter(Directory.user_id == current_user.id):
            text.append({"name": i.name, "id": f"/save/{str(num) + ';' + str(i.id)}"})
    else:
        title = "Переместить в"
        for i in db_sess.query(Directory).filter(Directory.user_id == current_user.id, Directory.id != tg.in_directory):
            text.append({"name": i.name, "id": f"/save/{str(num) + ';' + str(i.id) + ';' + str(tg.in_directory)}"})
    return render_template("dir.html", title=title, text=text)
@app.route("/save/<nums>")
def cr3(nums):
    nums = nums.split(";")
    db_sess = db_session.create_session()
    tg = db_sess.query(Tags_of_map).filter(Tags_of_map.id == nums[0]).first()
    dir = db_sess.query(Directory).filter(Directory.id == nums[1]).first()
    tg_id = tg.id
    if len(nums) == 3:
        old_dir = db_sess.query(Directory).filter(Directory.id == nums[2]).first()
        new_id = ""
        tags = old_dir.tags.split(";")
        for i in tags:
            if str(i) != str(tg_id) and i != "":
                new_id += f"{i};"
        old_dir.tags = new_id
        db_sess.commit()
    tg.in_directory = dir.id
    dir.tags = dir.tags + str(tg_id) + ";"
    db_sess.commit()
    return redirect("/blog/-1")
if __name__ == '__main__':
    db_session.global_init("db/Users.db")
    app.run(port=8080, host='127.0.0.1')
