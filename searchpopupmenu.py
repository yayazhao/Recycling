from kivymd.uix.dialog import MDInputDialog
from urllib import parse
from kivy.network.urlrequest import UrlRequest
from kivy.app import App
import certifi
from kivy.clock import Clock

class SearchPopupMenu(MDInputDialog):
    title = 'Type in Waste and Address separated by || then Search'
    hint_text = '''Waste Keyword e.g. plastic ; Address e.g. Charlotte, NC'''
    text_button_ok = 'Search'
    text_button_cancel = 'Cancel'
    auto_dismiss = False

    def __init__(self):
        super().__init__()
        self.hint_text = '''Waste Keyword e.g. plastic || Address e.g. Charlotte, NC'''
        self.size_hint = [.9, .3]
        self.events_callback = self.callback

    def open(self):
        super().open()
        Clock.schedule_once(self.set_field_focus, 0.5)

    def callback(self, *args):
        text = self.text_field.text
        if text and '||' in text:
            waste, address = text.split('||')
            App.get_running_app().settings.search_word = waste.strip()
            self.geocode_get_lat_lon(address.strip())

    def geocode_get_lat_lon(self, address):
        with open('api_key.txt', 'r') as f:
            api_key = f.read()
        address = parse.quote(address)
        url = "https://geocode.search.hereapi.com/v1/geocode?q=%s&apiKey=%s"%(address, api_key)
        UrlRequest(url, on_success=self.success, on_failure=self.failure, on_error=self.error, ca_file=certifi.where())

    def success(self, urlrequest, result):
        print("Success")
        latitude = result['items'][0]['position']['lat']
        longitude = result['items'][0]['position']['lng']
        app = App.get_running_app()
        mapview = app.root.ids.mapview
        mapview.center_on(latitude, longitude)
        App.get_running_app().settings.reset()

    def error(self, urlrequest, result):
        print("error")
        print(result)

    def failure(self, urlrequest, result):
        print("failure")
        print(result)

