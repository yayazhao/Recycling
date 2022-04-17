from kivymd.uix.dialog import ListMDDialog

class LocationPopupMenu(ListMDDialog):
    def __init__(self, facility_data):
        super().__init__()

        # Set all of the fields of market data
        headers = "ID,Name,Phone,Street,City,State,Zip,Lat,Lng"
        headers = headers.split(',')

        for i in range(len(headers)):
            attribute_name = headers[i]
            attribute_value = facility_data[i]
            setattr(self, attribute_name, str(attribute_value))