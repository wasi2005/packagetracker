from fedex import FedexPackage
from ups import UPSPackage
from usps import USPSPackage

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

wasi = Package(parcel_number = "9400109205568095615520", carrier = "USPS")
print (wasi.get_status())
