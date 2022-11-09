import math
import urllib.request
import urllib.parse

class FilterData:
    def __init__(self, data) -> None:
        self.purple_data = data
        pass
    def aqi_value(self, concentration: int | float):
        aqi = 0
        if concentration  >= 0 and concentration < 12.1:
            aqi = concentration * 4.1666666
        elif concentration  >= 12.1 and concentration < 35.5:
            aqi = ((concentration-12.1) * 2.103) + 51
        elif concentration  >= 35.5 and concentration < 55.5:
            aqi = ((concentration-35.5) * 2.4623) + 101
        elif concentration  >= 55.5 and concentration < 150.5:
            aqi = ((concentration-55.5) * 0.516333) + 151
        elif concentration  >= 150.5 and concentration < 250.5:
            aqi = ((concentration-150.5) * .99099) + 201
        elif concentration  >= 250.5 and concentration < 350.5:
            aqi = ((concentration-250.5) * .99099) + 301
        elif concentration  >= 350.5 and concentration < 500.5:
            aqi = ((concentration-350.5) * .66044) + 401
        else:
            aqi = 501
        return round(aqi)

    def find_distance(self, pointOne: float, pointTwo: float, distance: int|float) -> bool:
        latOne = pointOne[0] / 57.29577951
        latTwo = pointTwo[0] / 57.29577951
        lonOne = pointOne[1] / 57.29577951
        lonTwo = pointTwo[1] / 57.29577951
        if (latOne > 0 and latTwo > 0) or (latOne < 0 and latTwo < 0):
            if latOne < latTwo:
                dlat = latTwo - latOne
                alat = abs(latOne+latTwo)/2
            else:
                dlat = latOne - latTwo
                alat = abs(latOne+latTwo)/2
        else:
            dlat = abs(latOne - latTwo)
            alat = dlat/2
        if lonOne < lonTwo:
            dlon = lonTwo - lonOne
        else:
            dlon = lonOne - lonTwo
        x = dlon * math.cos(alat)
        d = (math.sqrt((x**2) + (dlat**2))) * 3958.8
        if d <= distance:
            return True
        else:
            return False
    
    def search_url(self, query: str, max: int, api_key: str, base_url: str) -> str:
        parameters = [
            ('key', api_key), ('part', 'snippet'),
            ('type', 'String'), ('maxResults', str(max)),
            ('q', query)
        ]
        return f'{base_url}/'

    def result(url: str, api_key: str):
        #for item in self.purple_data['data']:
        #    if find_distance() < miles and 

        response = None
        try:
            request = urllib.request.Request(
            url,
            headers = {'X-API-Key': api_key})
            response = urllib.request.urlopen(request)
            data = response.read().decode(encoding = 'utf-8')
            return data
        finally:
            if response != None:
                response.close()