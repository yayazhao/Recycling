from enum import Enum
from kivy.app import App
from facilitymarker import FacilityMarker

class Goal(Enum):
    BUY = 1
    DONATE = 2
    RECYCLE = 3


class AppSettings():
    goal = Goal.RECYCLE
    recycle_facility_ids = []
    donate_facility_ids = []
    buy_facility_ids = []
    search_word = ''

    def reset(self):
        self.recycle_facility_ids = []
        self.donate_facility_ids = []
        self.buy_facility_ids = []
        App.get_running_app().root.ids.mapview.clear_markers()
        App.get_running_app().root.ids.mapview.get_facilities_in_fov()

    def change_goal(self, goal: Goal):
        self.goal = goal
        self.reset()

    def get_facility_ids(self):
        if self.goal == Goal.RECYCLE:
            return self.recycle_facility_ids
        elif self.goal == Goal.DONATE:
            return self.donate_facility_ids
        else:
            return self.buy_facility_ids

    def get_facilities(self, min_lat, min_lon, max_lat, max_lon):
        print(f'Search Word: {self.search_word}.')
        app = App.get_running_app()
        if self.goal == Goal.RECYCLE:
            return app.r3dao.search_recycle_by_waste(self.search_word, min_lon=min_lon, max_lon=max_lon, min_lat=min_lat, max_lat=max_lat)
        elif self.goal == Goal.DONATE:
            return app.r3dao.search_reuse('', goal='Donate', min_lon=min_lon, max_lon=max_lon, min_lat=min_lat, max_lat=max_lat)
        else:
            return app.r3dao.search_reuse('', goal='Buy', min_lon=min_lon, max_lon=max_lon, min_lat=min_lat, max_lat=max_lat)
