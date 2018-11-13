from pymongo import MongoClient
import smtplib
from monitors.no_communication_with_buoy import *
from monitors.battery_is_low import *

monitors = ["no_communication_with_buoy", "battery_is_low"]


def send_notification(alert_obj):

    receiver = alert_obj["receiver"]
    body = alert_obj["body"]
    subject = alert_obj["subject"]

    sender = 'themo@univ.haifa.ac.il'

    message = "\r\n".join([
        "From: themo@univ.haifa.ac.il",
        "To: %s" % receiver,
        "Subject: Themo alert:  %s" % subject,
        "",
        "%s" % body,
        "",
        "",
        """
        """
    ])

    try:
       smtpObj = smtplib.SMTP('mr1.haifa.ac.il', 25)
       smtpObj.sendmail(sender, receiver, message)
       print("-I- Successfully sent email")
    except SMTPException:
       print("-E- Error: unable to send email")


def init_db():
    print("-I- Connecting to MOngo DB...")

    global client; client = MongoClient()
    global db; db = client.themo


if __name__ == "__main__":
    init_db()
    for monitor in monitors:
        print("\n-I- running '{0}'".format(monitor))
        alert_obj = globals()[monitor](db)
        if alert_obj:
            send_notification(alert_obj)
