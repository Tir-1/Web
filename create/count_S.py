import requests
import math
a = ""
b = ""

def lonlat_distance(a, b):
    degree_to_meters_factor = 111 * 1000
    a_lon, a_lat = a
    b_lon, b_lat = b
    a_lon, a_lat, b_lon, b_lat = float(a_lon), float(a_lat), float(b_lon), float(b_lat)
    radians_lattitude = math.radians((a_lat + b_lat) / 2.)
    lat_lon_factor = math.cos(radians_lattitude)
    dx = abs(a_lon - b_lon) * degree_to_meters_factor * lat_lon_factor
    dy = abs(a_lat - b_lat) * degree_to_meters_factor
    distance = math.sqrt(dx * dx + dy * dy)
    return distance


def coordinates(locals):
    l = []
    locals.split(";")
    geocoder_request = "http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode=&format=json"
    for i in locals:
        geocoder_request = f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={i}&format=json"
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
            # Печатаем извлечённые из ответа поля:
            l.append(toponym_coodrinates)
        else:
            print("Ошибка выполнения запроса:")
            print(geocoder_request)
    return lonlat_distance(l[0].split(), l[1].split())
#l = coordinates(["Москва", "Минск"])
#print(lonlat_distance(l[0].split(), l[1].split()))