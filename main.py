from kivymd.app import MDApp
from dao import R3Dao
from app_settings import AppSettings, Goal
from facilitiesmapview import FacilitiesMapView
from searchpopupmenu import SearchPopupMenu
from gpshelper import GpsHelper
from voice_assistant import VoiceAssistant


class MainApp(MDApp):
    r3dao = None
    search_menu = None
    settings = None
    gps_helper = None
    va = None
    msg_queue = None

    def on_start(self):
        self.theme_cls.primary_palette = 'BlueGray'

        # Initialize default settings
        self.settings = AppSettings()

        # Initialize GPS
        self.gps_helper = GpsHelper()
        self.gps_helper.run()

        # Connect to database
        self.r3dao = R3Dao()

        # Instantiate SearchPopupMenu
        self.search_menu = SearchPopupMenu()



    def change_goal(self, goal: int):
        goal = Goal.BUY if goal == 1 else Goal.DONATE if goal == 2 else Goal.RECYCLE
        self.settings.change_goal(goal)

    def recenter(self):
        self.gps_helper.has_centered_map = False
        self.settings.reset()

    def flip_va(self):
        print('Toggle voice assistant')
        if not self.va:
            self.va = VoiceAssistant()
            self.va.wastes.extend(['paper', 'car', 'printer', 'laptop', 'desktop', 'computer', 'toy'])
            self.va.run()
        if self.va.stop:
            self.va.stop = True
            del self.va
            self.va = None


MainApp().run()

