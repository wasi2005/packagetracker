import requests
import json

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
