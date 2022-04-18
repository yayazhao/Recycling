import os
import time
import playsound as ps
import speech_recognition as sr
from gtts import gTTS
import threading
import psutil

SOUND_FILE = {
    'greeting': 'sound_greeting.mp3',
    'again': 'sound_again.mp3',
    'bye': 'sound_bye.mp3',
    'search': 'sound_search.mp3',
}


def say(text):
    if text in SOUND_FILE:
        file_name = os.path.join(os.path.dirname(__file__), SOUND_FILE[text]).strip()
        ps.playsound(file_name)


def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ''
        try:
            said = r.recognize_google(audio)
        except Exception as e:
            print("Exception: " + str(e))
    return said.lower()


class VoiceAssistant(threading.Thread):
    stop = False
    def run(self):
        say('greeting')
        while True:
            if self.stop:
                say('bye')
                print('I am off')
                break
            print('I am ready')
            _text = get_audio()
            print(_text)

# if __name__ == '__main__':
#     speak('Hello, how are you? What can I do for you?', 'sound_greeting.mp3')
#     speak('Bye-bye?', 'sound_bye.mp3')
#     speak('I could not understand you. Please say a waste type again to search.', 'sound_again.mp3')
#     speak('Great. I am going to search for you.', 'sound_search.mp3')