from kivy_garden.mapview import MapView
from kivy.clock import Clock
from kivy.app import App
from facilitymarker import FacilityMarker


class FacilitiesMapView(MapView):
    getting_facilities_timer = None
    marker_list = set()

    def start_getting_facilities_in_fov(self):
        # after 1 sec, get the facilities in the field of view (fov)
        try:
            self.getting_facilities_timer.cancel()
        except:
            pass

        self.getting_facilities_timer = Clock.schedule_once(self.get_facilities_in_fov, 1)

    def get_facilities_in_fov(self, *args):
        # Get reference to main app and the database cursor
        min_lat, min_lon, max_lat, max_lon = self.get_bbox()
        print(min_lat, min_lon, max_lat, max_lon)
        app = App.get_running_app()

        facilities = app.settings.get_facilities(min_lon=min_lon, max_lon=max_lon, min_lat=min_lat, max_lat=max_lat)
        facility_ids = app.settings.get_facility_ids()
        # print(facilities)
        for facility in facilities:
            id = facility[0]
            if id in facility_ids:
                continue
            else:
                self.add_facility(facility, facility_ids)

    def add_facility(self, facility, facility_ids):
        lat, lon = facility[-2], facility[-1]
        marker = FacilityMarker(lat=lat, lon=lon, source='poi_red.png')
        marker.facility_data = facility
        # Add the MarketMarker to the map
        self.add_marker(marker)
        self.marker_list.add(marker)

        # Keep track of the marker's id
        id = facility[0]
        facility_ids.append(id)

    def clear_markers(self):
        for marker in self.marker_list:
            self.remove_marker(marker)
        self.marker_list = set()

