import json
import urllib.request
from pathlib import Path

class ReverseGeocoding:
    def __init__(self) -> None:
        self.geoLocation = None

    def getAddress(self):
        return self.geoLocation
    

class NominatimReverse(ReverseGeocoding):
    def __init__(self, lat: int|float, lon: int|float) -> None:
        self.lat = lat
        self.lon = lon

    def getAddress(self):
        self.apiUrl = "https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat={lat}&lon={lon}".format(lat = self.lat, lon = self.lon)
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
        address = obj['display_name']
        return address

class FileReverseGeoCoding(ReverseGeocoding):
    def __init__(self, file) -> None:
        self.geoFile = file
    
    def getAddress(self):
        with open(self.geoFile) as file:
            contents = file.read()
            obj = json.loads(contents)
            address = obj['display_name']
            return address
    
    def getLat(self):
        with open(self.geoFile) as file:
            contents = file.read()
            obj = json.loads(contents)
            lat = obj['lat']
            return lat

    def getLon(self):
        with open(self.geoFile) as file:
            contents = file.read()
            obj = json.loads(contents)
            lon = obj['lon']
            return lon