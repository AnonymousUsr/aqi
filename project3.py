import math
from msilib import sequence
import urllib.request
import urllib.parse
import json
from pathlib import Path
from collections import namedtuple
import foward_geocoding
import reverse_geocoding
import aqi_data
import filter_data

Location = namedtuple('Location', ['location', 'miles', 'aqi', 'numLocations', 'keyOrPath', 'reverseGeocoding'])

class Controller:
    def __init__(self):
        self.info = {}
    def take_input(self):
        location = input('')
        splitLocation = location.split(' ')
        if splitLocation[0].upper() != 'CENTER':
            return 'Error'
        self.info['center'] = splitLocation[1:]
        if splitLocation[1] == 'NOMINATIM':
            furtherSplit = location.split('NOMINATIM ')
            lat_lon = foward_geocoding.NominatimGeocoding(furtherSplit[1])
            lat, lon = lat_lon.getGeoLocation()
            self.info['lat'] = lat
            self.info['lon'] = lon
        elif splitLocation[1].upper() == 'FILE':
            lat_lon = foward_geocoding.FileForwardGeoCoding(splitLocation[2])
            lat, lon = lat_lon.getGeoLocation()
            self.info['lat'] = lat
            self.info['lon'] = lon
        else:
            return 'Error'
        
        miles = input('')
        splitMiles = miles.split(' ')
        if int(splitMiles[1]) < 0 or splitMiles[0].upper() != 'RANGE':
            return 'Error'
        self.info['miles'] = int(splitMiles[1])

        aqi = (input(''))
        splitAQI = aqi.split(' ')
        if float(splitAQI[1]) < 0 or splitAQI[0].upper() != 'THRESHOLD':
            return 'Error'
        self.info['aqi'] = float(splitAQI[1])

        numLocations = (input(''))
        splitNumLocations = numLocations.split(' ')
        if splitNumLocations[0].upper() != 'MAX':
            return 'Error'
        self.info['max'] = splitNumLocations[1]

        keyOrPath = input('')
        splitKeyOrPath = keyOrPath.split(' ')
        if splitKeyOrPath[1].upper() == 'PURPLEAIR':
            self.info['key'] = splitKeyOrPath[2]
            try:
                purpleData = aqi_data.PurpleData(splitKeyOrPath[2])
                pa_data = purpleData.getData()
                self.info['data'] = pa_data
            except:
                print('Invalid key.')
        elif splitKeyOrPath[1].upper() == 'FILE':
            purpleDataFile = aqi_data.PurpleFileData(splitKeyOrPath[2])
            pa_data = purpleDataFile.getData()
            self.info['path'] = splitKeyOrPath[2]
            self.info['data'] = pa_data
        else: 
            return 'Error'
        
        reverseGeocoding = input('')
        self.info['reverseInput'] = reverseGeocoding
        
        print('CENTER ', end = '')
        self.formatPrint(None, float(self.info['lat']), float(self.info['lon']), None)
        return 'Good'

    def findFieldIndex(self, fieldName : str) -> int:
        count = 0
        for item in self.info['data']['fields']:
            if str(item).upper() == fieldName.upper():
                return count
            count += 1
        return -1
    
    def formatPrint(self, address: str, lat: float, lon: float, aqi: int|float) -> None:
        if aqi != None:
            print('AQI ' + str(aqi)) 
        if lat != None and lon != None:    
            if lat >= 0:
                print(str(lat) + '/N ', end = '')
            else:
                print(str(abs(lat)) + '/S ', end = '')
            if lon >= 0:
                print(str(lon) + '/E ')
            else:
                print(str(abs(lon)) + '/W ')  
        if address != None: 
            print(address)
    
    def process(self):
        moreCount = 0
        latIndex = self.findFieldIndex("latitude")
        lonIndex = self.findFieldIndex('longitude')
        pmIndex = self.findFieldIndex('pm2.5')
        goodLocations = []
        for itemData in self.info['data']['data']:
            fullData = filter_data.FilterData(itemData)
            pointOne = [float(self.info['lat']), float(self.info['lon'])]
            pointTwo = [itemData[latIndex], itemData[lonIndex]]
            if itemData[pmIndex] != None:
                aqi = fullData.aqi_value(itemData[pmIndex])
            else:
                aqi = -1
            if pointTwo != [None, None]:
                if (fullData.find_distance(pointOne, pointTwo, self.info['miles'])and 
                    (aqi >= self.info['aqi'])):
                    goodLocations.append(itemData)
        splitGeocoding = self.info['reverseInput'].split(' ')
        if len(splitGeocoding) == 2:
            for location in goodLocations[moreCount:]:
                if moreCount >= int(self.info['max']):
                    break
                try:
                    address = reverse_geocoding.NominatimReverse(float(goodLocations[moreCount][latIndex]), float(goodLocations[moreCount][lonIndex]))
                    exactLocation = address.getAddress()
                    new_aqi = fullData.aqi_value(location[pmIndex])
                    self.formatPrint(exactLocation, float(goodLocations[moreCount][latIndex]), float(goodLocations[moreCount][lonIndex]), float(new_aqi))
                    moreCount += 1
                except:
                    print('Unable to find locations.')
        elif splitGeocoding[1] == 'FILES' and len(splitGeocoding[2:]) >= int(self.info['max']):
            for file in splitGeocoding[2:]:
                for location in goodLocations[moreCount:]:
                    try:
                        reverseAddress = reverse_geocoding.FileReverseGeoCoding(file)
                        exactLocation = reverseAddress.getAddress()
                        new_aqi = fullData.aqi_value(location[pmIndex])
                        self.formatPrint(exactLocation, float(goodLocations[moreCount][latIndex]), float(goodLocations[moreCount][lonIndex]), float(new_aqi))
                        moreCount += 1
                        break
                    except:
                        print(file + ' is not a valid file')

if __name__ == '__main__':
    start = Controller()
    result = start.take_input()
    if result == 'Error':
        print('Input Error')
    else:
        start.process()
    