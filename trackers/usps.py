# https://tools.usps.com/go/TrackConfirmAction?tRef=fullpage&tLc=3&text28777=&tLabels=9400109205568095615520
import requests
import json
from bs4 import BeautifulSoup

class USPSPackage(object):
    parcel_number = ''

    def __init__(self, parcel_number):
        self.parcel_number = parcel_number

    def get_status(self):
        service_endpoint = 'https://tools.usps.com/go/TrackConfirmAction'
        tracking_request = {
            "headers" : {
                "User-Agent" : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36',
                "Content-Type" : "application/x-www-form-urlencoded"
            },
            "data" : {
                "tRef": "fullpage",
                "tLc": "3",
                "text28777": "",
                "tLabels" : self.parcel_number
            }
        }

        response = BeautifulSoup(requests.post(service_endpoint, data="tRef=fullpage&tLc=3&text28777=&tLabels=9400109205568095615520", headers=tracking_request['headers'], allow_redirects=True).text, "html.parser")
        status = response.find("div", {"class": "delivery_status"}).find("strong").encode_contents().decode('UTF-8').upper()

        status_code = -1
        if status == "ACCEPTANCE" or status == "ELECTRONIC SHIPPING INFO RECEIVED":
            status_code = 0
        elif status == "PROCESSED THROUGH SORT FACILITY" :
            status_code = 1
        elif status == "IN TRANSIT" or status == "ARRIVAL AT UNIT" or status == "OUT-FOR-DELIVERY":
            status_code = 2
        elif status == "DELIVERED":
            status_code = 3
        else:
            status_code = -1
        return status_code
