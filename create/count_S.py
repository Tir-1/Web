import requests
import math

a = ""
b = ""


def lonlat_distance(a, b, tp):  # высчитывает дистанцию
    degree_to_meters_factor = 111 * 1000
    a_lon, a_lat = a
    b_lon, b_lat = b
    a_lon, a_lat, b_lon, b_lat = float(a_lon), float(a_lat), float(b_lon), float(b_lat)
    radians_lattitude = math.radians((a_lat + b_lat) / 2.)
    lat_lon_factor = math.cos(radians_lattitude)
    dx = abs(a_lon - b_lon) * degree_to_meters_factor * lat_lon_factor
    dy = abs(a_lat - b_lat) * degree_to_meters_factor
    distance = math.sqrt(dx * dx + dy * dy)
    return f"Расстоние между {tp[0]} и {tp[1]} равно {distance}"


def coordinates(locals):  # находит координаты двух объектов
    l = []
    locals = locals.split(";")
    tp = []
    for i in locals:
        geocoder_request = f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode=" \
                           f"{i}&format=json"
        response = requests.get(geocoder_request)
        try:
            if response:
                json_response = response.json()
                toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
                toponym_address = toponym["metaDataProperty"]["GeocoderMetaData"]["text"]
                tp.append(toponym_address)
                toponym_coodrinates = toponym["Point"]["pos"]
                l.append(toponym_coodrinates)
            else:
                print("Ошибка выполнения запроса:")
                print(geocoder_request)
        except:
            return False
    return lonlat_distance(l[0].split(), l[1].split(), tp)
