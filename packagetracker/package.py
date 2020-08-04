import requests
import json
from bs4 import BeautifulSoup

#start of fedex track system
class FedexPackage(object):

    parcel_number = ""

    def __init__(self, parcel_number):
        self.parcel_number = parcel_number

    def get_status(self):
        service_endpoint = "https://www.fedex.com/trackingCal/track"

        tracking_request = {
            "data": json.dumps({
                "TrackPackagesRequest": {
                    "appType": "wtrk",
                    "uniqueKey": "",
                    "processingParameters": {
                        "anonymousTransaction": True,
                        "clientId": "WTRK",
                        "returnDetailedErrors": True,
                        "returnLocalizedDateTime": False
                    },
                    "trackingInfoList": [{
                        "trackNumberInfo": {
                            "trackingNumber": self.parcel_number,
                            "trackingQualifier": "",
                            "trackingCarrier": ""
                        }
                    }]
                }
            }),
            "action": "trackpackages",
            "locale": "en_US",
            "format": "json",
            "version": 99
        }

        status_code = -1
        status = requests.post(service_endpoint, data=tracking_request).json()['TrackPackagesResponse']['packageList'][0]['keyStatus'].upper()
        if status == "INITIATED":
            status_code = 0
        elif status == "PICKED UP":
            status_code = 1
        elif status == "IN TRANSIT":
            status_code = 2
        elif status == "DELIVERED":
            status_code = 3
        else:
            status_code = -1
        return status_code

#start of ups track system
class UPSPackage(object):
    parcel_number = ''

    def __init__(self, parcel_number):
        self.parcel_number = parcel_number

    def get_status(self):
        service_endpoint = 'https://www.ups.com/track/api/Track/GetStatus'
        tracking_request = {
            "headers" : {
                "Content-Type" : "application/json"
            },
            "data" : json.dumps({
                "Locale": "en_US",
                "TrackingNumber": [self.parcel_number]
            })
        }

        status = requests.post(service_endpoint, data=tracking_request['data'], headers=tracking_request['headers']).json()['trackDetails'][0]['packageStatus'].upper()

        status_code = -1
        if status == "ORIGIN SCAN" or status == "ORDER PROCESSED: READY FOR UPS" or status == "ORDER PROCESSED: IN TRANSIT TO UPS" or status == "DROPPED OFF AT A UPS ACCESS POINT™ LOCATION" or status == "DROPPED OFF AT THE UPS STORE®":
            status_code = 0
        elif status == "ARRIVAL SCAN" or status == "DEPARTURE SCAN" :
            status_code = 1
        elif status == "DESTINATION SCAN" or status == "IN TRANSIT" or status == "ON VEHICLE FOR DELIVERY/OUT FOR DELIVERY":
            status_code = 2
        elif status == "DELIVERED":
            status_code = 3
        else:
            status_code = -1
        return status_code

#start of usps track system
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

#start of universal track system
class Package(object):
     parcel_number = ""
     carrier = ""

     def __init__(self, parcel_number, carrier):
         self.parcel_number = str(parcel_number)
         self.carrier = carrier.upper()

     def get_status(self):
         package = None
         if self.carrier == "FEDEX":
             package = FedexPackage(self.parcel_number)
         elif self.carrier == "UPS":
             package = UPSPackage(self.parcel_number)
         elif self.carrier == "USPS":
             package = USPSPackage(self.parcel_number)
         else:
             return "Sorry, we only support USPS, UPS, or Fedex."
         return package.get_status()
