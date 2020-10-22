#Import Requests for POST Method
import requests


def sendsms(txt):
    #Define The URL We Wanna Post to
    url = "https://www.sms4free.co.il/ApiSMS/SendSMS"

    #Declear Some Variables
    key = "SdEu334KH"
    user = "0529434220"
    _pass = "92921327"
    sender = "Themo"
    recipient = "0529434220;0547885797;0549259989"
    # recipient = "0547885797"
    msg = txt

    #Object that have the data we wanna POST
    data = {}

    data["key"] = key
    data["user"] = user
    data["pass"] = _pass
    data["sender"] = sender
    data["recipient"] = recipient
    data["msg"] = msg

    #Post Data
    response = requests.post(url, json= data)

    print(response) #Should GET Status 200 (SUCCESS)


if __name__ == "__main__":
    txt = "אוי ואבוי המצוף ברח"
    sendsms(txt)
