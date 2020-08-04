import requests
import json

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
