import json
import urllib.request
from pathlib import Path

class ForwardGeoCoding:
    def __init__(self) -> None:
        self.geoLocation = None

    def getGeoLocation(self):
        return self.geoLocation

class NominatimGeocoding(ForwardGeoCoding):
    def __init__(self, address) -> None:
        self.address = address

    def getGeoLocation(self):
        self.apiUrl = "https://nominatim.openstreetmap.org/search/{}?format=json&addressdetails=1&limit=1".format(self.address)
        self.apiUrl = self.apiUrl.replace(" ", "%20")
        try:
            request = urllib.request.Request(self.apiUrl)
            response = urllib.request.urlopen(request)
            data = response.read().decode(encoding = 'utf-8')
        except:
            print("FAILED\n{}\nNETWORK".format(self.apiUrl))
        finally:
            response.close()
        obj = json.loads(data)
        lon = obj[0]['lon']
        lat = obj[0]['lat']
        return lat, lon
        
class FileForwardGeoCoding(ForwardGeoCoding):
    def __init__(self, file) -> None:
        self.geoFile = file
    
    def getGeoLocation(self):
        with open(self.geoFile) as file:
            contents = file.read()
            obj = json.loads(contents)
            lon = obj[0]['lon']
            lat = obj[0]['lat']
            return lat, lon

