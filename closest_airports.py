
import csv
import math
import sys
import json
from math import radians, cos, sin, asin, sqrt
maxInt = sys.maxsize

while True:
    # decrease the maxInt value by factor 10
    # as long as the OverflowError occurs.
    try:
        csv.field_size_limit(maxInt)
        break
    except OverflowError:
        maxInt = int(maxInt/10)

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance in kilometers between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.
    return c * r

class ClosestAirport:

    def __init__(self, dist_function="haversine"):
        self.airports = json.load(open('data/airports.json'))

        # This is not redundant - allows for more dist functions in future
        if dist_function == "haversine":
            self.dist_function = haversine
        else:
            self.dist_function = haversine

    """
    Input: latitude, longitude
    Output: IATA of closest airport
    """
    def find_closest(self, lat, long):
        best_iata = ""
        lowest_dist = math.inf
        for airport in self.airports:
            coords = airport["geolocation"]["coordinates"]
            dist = self.dist_function(lat, long, coords[0], coords[1])
            if dist < lowest_dist:
                best_iata = airport["iata"]
                lowest_dist = dist
        return best_iata

    def update_events(self):
        with open('data/events.csv', newline='', encoding='utf-8') as csvfile:
            r = csv.DictReader(csvfile, delimiter=',', quotechar='"')
            rows=[]
            for event in r:
                closest_iata = self.find_closest(float(event['lat']), float(event['lng']))
                event['closest_iata'] = closest_iata
                rows.append(event)
                fields = list(r.fieldnames)
                fields.append('closest_iata')

        print(rows)

        with open("data/events1.csv", "w", newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.DictWriter(csvfile, fieldnames=fields)
            csv_writer.writeheader()
            csv_writer.writerows(rows)


if __name__ == '__main__':
    updater = ClosestAirport()
    updater.update_events()









