import requests
from flask_login import current_user
# Находит изображение указаного места


def start(x, check):
    lon, lat, Z = 0, 0, 10
    l = 'sat'
    n = x.split(";")
    geocoder_request = f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode=" \
                       f"{n[0]},1&format=json"
    if len(n) > 1:
        Z = int(n[1])
        Z += check
        if n[2] == "Карта":
            l = "map"
        elif n[2] == "Спутник":
            l = "sat"
        else:
            l = "sat,skl"
    response = requests.get(geocoder_request)
    try:
        if response:
            json_response = response.json()
            toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
            toponym_address = toponym["metaDataProperty"]["GeocoderMetaData"]["text"]
            toponym_coodrinates = toponym["Point"]["pos"]
            toponym_coodrinates = toponym_coodrinates.split()
            get_image(toponym_coodrinates[0], toponym_coodrinates[1], Z, l)
            return str(toponym_address)
    except:
        return False


def get_image(lon, lat, z, l):
    WIDTH, HEIGHT = 450, 450
    params = {
        'l': l,
        'll': ','.join([str(lon), str(lat)]),
        'z': str(z),
        'size': ','.join([str(WIDTH), str(HEIGHT)])
    }
    request = requests.get('https://static-maps.yandex.ru/1.x/', params)
    print(request.content)
    with open(f'static/{current_user.name}.png', 'wb') as file:
        file.write(request.content)
