import requests

class Vehicle(object):
    
    def __init__(self, jsonArgs, route=None):

        self.latitude    = float(jsonArgs['lat'])
        self.longitude   = float(jsonArgs['lng'])
        self.coords      = (self.latitude, self.longitude)

        self.vehicleID   = jsonArgs['VehicleID']
        self.blockID     = jsonArgs['BlockID']
        self.label       = jsonArgs['label']
        self.direction   = jsonArgs['Direction']

        self.title       = self.label
        self.offset      = jsonArgs['Offset']
        self.destination = jsonArgs['destination']
        self.route       = route
     

def getVehiclesByRoute(routeIdentifier):        
    vehicleURL = "http://www3.septa.org/beta/TransitView/" + routeIdentifier
    r = requests.get(vehicleURL)
    j = r.json()
    vehicles = j['bus']
    return [Vehicle(v, route=routeIdentifier) for v in vehicles]


with open("targetRoutes.txt") as t:
    route_list = t.read()
    route_list = route_list.split()
    route_list = set(route_list)


vehicle_list = [getVehiclesByRoute(r) for r in route_list]

# Flattening vehicle list
vehicle_list = [x for sublist in vehicle_list for x in sublist]

with open("vehicle_numbers.txt") as v:
    my_busses = v.read()
    my_busses = my_busses.split()
   
vehicle_list = [a for a in vehicle_list if a.vehicleID in my_busses]


report_string = "Bus #    Route\n"

for b in vehicle_list:
    report_string += b.vehicleID + "      " + b.route + "\n"

with open("report.txt", "w") as w:
    w.write(report_string)


