# import urllib.request
from urllib.request import Request, urlopen
import json
from datetime import datetime
import geopy.distance

MAX_HOURS_ALLOWED_FROM_LAST_REPORT = 2
MAX_DISTANCE_ALLOWED_KM = 1

def geturl():
    base_url = 'https://services.marinetraffic.com/api/exportvessels/v:8/'
    api_key = '0843643edb328b02bb0e525cb07ec8f106a9cbd7'
    # mmsi = '/mmsi:244010235'
    # mmsi = '/mmsi:994280102'
    timespan = '/timespan:2880'
    protocol = '/protocol:json'
    global url; url = base_url + api_key + timespan + protocol
    if __name__ == '__main__':
        print(url)


def openurl():
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})

    try:
        global data; data = json.loads(urlopen(req).read().decode('utf-8'))
    except Exception as ex:
        print("-e- failed to load json from url")
        print("-e- exception: " + str(ex))
        data = [["244010235","0","5689729","33.039230","34.947150","6","511","207","99","2020-10-21T11:00:25","TER","20"]]


    if __name__ == '__main__':
        print(data)

    global lat; lat = data[0][3]
    global lon; lon = data[0][4]
    global when; when = data[0][9]


def create_alert_obj(text):
    alert_obj = {}
    alert_obj["receiver"] = [ "imardix@univ.haifa.ac.il", "sdahan3@univ.haifa.ac.il", "lnagar1@univ.haifa.ac.il"]
    # alert_obj["receiver"] = [ "imardix@univ.haifa.ac.il"]
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

    if delta_in_hours >= MAX_HOURS_ALLOWED_FROM_LAST_REPORT:
        text = "No AIS report recieved during the last {0} hours".format(MAX_HOURS_ALLOWED_FROM_LAST_REPORT)
        return create_alert_obj(text)


def check_runaway(db):
    ref_coord = (33.039230, 34.947150) #this is our ref-point
    last_coord = (lat, lon)
    # distance = geopy.distance.vincenty(ref_coord, last_coord).km - Removed geopy.distance.vincenty, use geopy.distance.geodesic instead.
    distance = geopy.distance.geodesic(ref_coord, last_coord).km
    distance = round(distance, 2)


    if __name__ == '__main__':
        print("distance to ref point: " + str(distance) + "km")
    if distance >= MAX_DISTANCE_ALLOWED_KM:
        text = "buoy reported location is {0}km from ref point".format(distance)
        if __name__ == '__main__':
            print(txt)
        text = text + "\npossible runaway??"
        return create_alert_obj(text)



if __name__ == '__main__':
    db = None
    check_when_was_last_ais(db)
    check_runaway(db)
