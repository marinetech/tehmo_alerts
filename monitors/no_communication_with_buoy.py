from datetime import datetime

MAX_HOURS_ALLOWED = 6


def no_communication_with_buoy(db):
    for buoy_name in ["tabs225m09"]:
        filter = {}
        filter["buoy"] = buoy_name
        for doc in db.samples.find(filter).sort([('d_stamp', -1), ('t_stamp', -1)]).limit(1):
            doc_datetime = datetime.strptime(doc["d_stamp"] + " " + doc["t_stamp"], '%Y-%m-%d %H:%M:%S')            
            now = datetime.now()
            delta = now - doc_datetime # timedelta obj
            delta_in_hours = delta.seconds / 3600



            if delta_in_hours > MAX_HOURS_ALLOWED:
                print("     delta_in_hours: " + str(delta_in_hours))
                print("     MAX_HOURS_ALLOWED: " + str(MAX_HOURS_ALLOWED))
                print("     Sending Alert...")
                return create_alert_obj(buoy_name)
            else:
                return None


def create_alert_obj(buoy):
    alert_obj = {}
    alert_obj["receiver"] = [ "imardix@univ.haifa.ac.il", "sdahan3@univ.haifa.ac.il" ]
    alert_obj["subject"] = "Themo Alert - No communication from: " + buoy
    alert_obj["body"] = "According to THEMO DB, No Communication was recieved from {0} during the last {1} Hours".format(buoy, MAX_HOURS_ALLOWED)
    return alert_obj
