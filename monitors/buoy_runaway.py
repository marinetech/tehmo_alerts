# import urllib.request
from urllib.request import Request, urlopen
import json
from datetime import datetime
import geopy.distance

MAX_HOURS_ALLOWED = 6
MAX_DISTANCE_ALLOWED = 2

def geturl():
    base_url = 'https://services.marinetraffic.com/api/exportvessel/v:5/'
    api_key = 'b28760950bcfd096d9e0767d416cee6a324c75cb'
    mmsi = '/mmsi:994280102'
    timespan = '/timespan:2880'
    protocol = '/protocol:json'
    global url; url = base_url + api_key + timespan + mmsi + protocol
    if __name__ == '__main__':
        print(url)

def openurl():
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    global data; data = json.loads(urlopen(req).read().decode('utf-8'))
    if __name__ == '__main__':
        print(data)
    global lat; lat = data[0][1]
    global lon; lon = data[0][2]
    global when; when = data[0][7]

    # print(data)
    # print('LAT: {0} LON: {1} TIME: {2}'.format(lat, lon, when))

def create_alert_obj(text):
    alert_obj = {}
    alert_obj["receiver"] = [ "imardix@univ.haifa.ac.il", "sdahan3@univ.haifa.ac.il" "lnagar1@univ.haifa.ac.il"]    
    alert_obj["subject"] = "AIS"
    alert_obj["body"] = text
    return alert_obj

def check_when_was_last_ais(db):
    geturl()
    openurl()
    now = datetime.utcnow()
    last_ais_report = datetime.strptime(when, '%Y-%m-%dT%H:%M:%S')
    delta = now - last_ais_report # timedelta obj
    delta_in_hours = int(delta.seconds / 3600)
    if __name__ == '__main__':
        print("last_ais_report: " + str(last_ais_report))
        print("delta_in_hours: " + str(delta_in_hours))
    if delta_in_hours >= MAX_HOURS_ALLOWED:
        text = "No AIS report recieved during the last {0} hours".format(MAX_HOURS_ALLOWED)
        return create_alert_obj(text)

    # print("last_ais_report: " + str(last_ais_report))
    # print("delta_in_hours: " + str(delta_in_hours))

def check_runaway(db):
    ref_coord = (32.801840, 34.385630) #this is our ref-point
    last_coord = (lat, lon)
    distance = geopy.distance.vincenty(ref_coord, last_coord).km
    if __name__ == '__main__':
        print("distance to ref point: " + str(distance))
    if distance >= MAX_DISTANCE_ALLOWED:
        text = "buoy reported location is {0}km from ref point".format(distance)
        text = text + "\npossible runaway??"
        return create_alert_obj(text)



if __name__ == '__main__':
    db = None
    check_when_was_last_ais(db)
    check_runaway(db)
