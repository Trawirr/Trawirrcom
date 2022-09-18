import reverse_geocoder as rg
import numpy as np  
from requests import get
from datetime import datetime

from BorsukUlam.models import BorsukUlamPoint
from mainapp.models import Variable

BASE = 'https://api.openweathermap.org/data/2.5/weather'
API_KEY = '00dbce25503eebf0535dd18a1dfb2ba7'
UNITS = 'metric'
LAT = 63.595
LON = 118.892

class BorsukUlam():
    def __init__(self) -> None:
        pass

    def get_random_coordinates(self):
        return (np.random.rand() * 180 - 90, np.random.rand() * 360 - 180)

    def get_antipodal_point(self, point):
        antipodal_point = lambda x, y: -np.sign(x - np.finfo(float).eps)*((-abs(x))%y)
        lat = -point[0]
        lon = antipodal_point(point[1], 180.0)
        return (lat, lon)

    def get_temperature_on_coordinates(self, point):
        data_temp = get(f'{BASE}?lat={point[0]}&lon={point[1]}&units={UNITS}&appid={API_KEY}').json()
        return data_temp['main']['temp']

    def get_next_point(self, point, val):
        diff1 = np.sign(np.random.rand()-.5) * np.random.rand()*val
        diff2 = np.sign(np.random.rand()-.5) * (val - abs(diff1))
        return (point[0] + diff1, point[1] + diff2)

    def get_nearest_city(self, point):
        return rg.search(point)[0]

    def get_distance_between_coordinates(self, point1, point2):
        R = 6371e3
        lat1, lon1 = point1
        lat2, lon2 = point2

        x1 = lat1 * np.pi/180
        x2 = lat2 * np.pi/180
        d1 = (lat2-lat1) * np.pi/180
        d2 = (lon2-lon1) * np.pi/180

        a = np.sin(d1/2) * np.sin(d1/2) + np.cos(x1) * np.cos(x2) * np.sin(d2/2) * np.sin(d2/2)
        c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))

        return R*c

    def get_diretction(self, point1, point2):
        direction = ""
        if point2[0] < point1[0]:
            direction += "N"
        else:
            direction += "S"
        if point2[1] < point1[1]:
            direction += "E"
        else:
            direction += "W"
        return direction

    def find_Borsuk_Ulam(self, threshold = .1):
        point = self.get_random_coordinates()
        while True:
            anti_point = self.get_antipodal_point(point)
            temp_diff = abs(self.get_temperature_on_coordinates(point) - self.get_temperature_on_coordinates(anti_point))
            print(f'Temp diff = {temp_diff:.2f} \'C')
            if temp_diff < threshold:
                city = self.get_nearest_city(point)
                city_anti = self.get_nearest_city(anti_point)
                city_distance = self.get_distance_between_coordinates(point, (float(city['lat']), float(city['lon'])))//10/100
                city_anti_distance = self.get_distance_between_coordinates(anti_point, (float(city_anti['lat']), float(city_anti['lon'])))//10/100
                direction = self.get_diretction(point, (float(city['lat']), float(city['lon'])))
                direction_anti = self.get_diretction(anti_point, (float(city_anti['lat']), float(city_anti['lon'])))

                bu1 = BorsukUlamPoint(
                    lat=point[0], 
                    lon=point[1], 
                    city=f"{city['name']}, {city['cc']}",
                    distance=city_distance, 
                    direction=direction,
                    temperature=self.get_temperature_on_coordinates(point)
                )
                bu2 = BorsukUlamPoint(
                    lat=anti_point[0], 
                    lon=anti_point[1], 
                    city=f"{city_anti['name']}, {city_anti['cc']}",
                    distance=city_anti_distance, 
                    direction=direction_anti,
                    temperature=self.get_temperature_on_coordinates(anti_point)
                )
                bu1.save()
                bu2.save()
                print(city)
                print(city_anti)
                info = f"Borsuk-Ulam found!\nPoint:           {point} - {city_distance}km from {city['name']}\nAntipodal point: {anti_point} - {city_anti_distance}km from {city_anti['name']}\nTemperature: {self.get_temperature_on_coordinates(point)}"
                print(info)
                last_update = Variable.objects.get(name="last borsuk ulam")
                last_update.value = datetime.now().strftime("%D %H:%M")
                last_update.save()
                break
            point = self.get_next_point(point, temp_diff)
            point = (point[0] if abs(point[0]) < 90 else point[0] + -np.sign(point[0])*180,
                    point[1] if abs(point[1]) < 180 else point[1] + -np.sign(point[1])*360)
            print(point, '\n')
