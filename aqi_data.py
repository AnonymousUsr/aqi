import json
import urllib.request

class AQI_Data():
    def __init__(self) -> None:
        pass
    def getData(self) -> dict:
        pass

class PurpleData(AQI_Data):
    def __init__(self, key: str) -> None:
        self.key = key
    def getData(self) -> dict:
        request = urllib.request.Request(
            'https://api.purpleair.com/v1/sensors?fields=name%2C%20latitude%2C%20longitude%2C%20pm2.5',
            headers = {'X-API-Key': self.key},
            method = 'GET')
        response = urllib.request.urlopen(request)
        data = response.read().decode(encoding = 'utf-8')
        obj = json.loads(data)
        return dict(obj)

class PurpleFileData(AQI_Data):
    def __init__(self, file) -> None:
        self.file = file
    def getData(self):
        with open(self.file) as file:
            contents = file.read()
            obj = json.loads(contents)
            return obj