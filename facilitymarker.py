from kivy_garden.mapview import MapMarkerPopup
from locationpopupmenu import LocationPopupMenu

class FacilityMarker(MapMarkerPopup):
    facility_data = []

    def on_release(self, *args):
        # Open up the LocationPopupMenu
        menu = LocationPopupMenu(self.facility_data)
        menu.size_hint = [.7, .7]
        menu.open()