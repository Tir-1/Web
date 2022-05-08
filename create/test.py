import sys

import requests
from flask_login import current_user

from data import db_session
from data.tags import Tags_of_map


def open_db():
    db_sess = db_session.create_session()
    lines = "&pt="
    for i in db_sess.query(Tags_of_map).filter(Tags_of_map.user_id == current_user.id):
        lines += str(i.coord) + "," + str(i.color)
        lines += "~"
    lines = lines[:-1]
    lines += "&"
    return lines

def load_map():
    n = open_db()
    print(n)
    if not n == "&pt&":
        map_request = f"http://static-maps.yandex.ru/1.x/?ll=-0.243073,-0.565456&l=map{n}z=1"
    else:
        map_request = "http://static-maps.yandex.ru/1.x/?ll=-0.243073,-0.565456&l=map&z=1"
    response = requests.get(map_request)
    if not response:
        sys.exit(1)
    with open(f'static/{current_user.name}.png', 'wb') as file:
        file.write(response.content)
