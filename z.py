lon, lat, Z = 0, 0, 10
WIDTH, HEIGHT = size = 450, 450
old_z = Z
l = 'map'
import requests
def start(x):
    geocoder_request = f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={x},1&format=json"
    response = requests.get(geocoder_request)
    if response:
        # Преобразуем ответ в json-объект
        json_response = response.json()

        # Получаем первый топоним из ответа геокодера.
        # Согласно описанию ответа, он находится по следующему пути:
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        # Полный адрес топонима:
        toponym_address = toponym["metaDataProperty"]["GeocoderMetaData"]["text"]
        # Координаты центра топонима:
        toponym_coodrinates = toponym["Point"]["pos"]
        toponym_coodrinates = toponym_coodrinates.split()

        get_image(toponym_coodrinates[0], toponym_coodrinates[1], Z, l)
        return str(toponym_address)



def get_image(lon, lat, z, l):
    params = {
        'l': l,
        'll': ','.join([str(lon), str(lat)]),
        'z': str(z),
        'size': ','.join([str(WIDTH), str(HEIGHT)])
    }
    request = requests.get('https://static-maps.yandex.ru/1.x/', params)
    with open('static/temporal.png', 'wb') as file:
        file.write(request.content)
