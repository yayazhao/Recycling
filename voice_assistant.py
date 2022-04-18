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

def close_if_open(fpath):
    pid = os.getpid()
    for proc in psutil.process_iter():
        try:
            if proc.pid == pid:
                print(proc.name())
                for item in proc.open_files():
                    if fpath in item.path:
                        print('fd: ', item.fd)
                        try:
                            proc.open_files().remove(item)
                            # os.close(item.fd)
                        except Exception as e:
                            print('Exception: ', str(e))
                            return False
        except Exception as e:
            print('Exception: ', str(e))
            return False
    return True


def say(text):
    if text in SOUND_FILE:
        file_name = os.path.join(os.path.dirname(__file__), SOUND_FILE[text]).strip()
        ps.playsound(file_name)


def speak(text, fname):
    tts = gTTS(text=text, lang='en')
    # fname = "voice.mp3"
    file_name = os.path.join(os.path.dirname(__file__), fname).strip()
    count = 0
    while True:
        try:
            tts.save(file_name)
            break
        except PermissionError as e:
            print(str(e))
            close_if_open(file_name)
            time.sleep(1)
            count += 1
            if count > 5:
                break
    ps.playsound(file_name)

    # delete the file, otherwise it may cause next save fail
    # if os.path.exists(file_name):
    #     os.remove(file_name)


def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ''
        try:
            said = r.recognize_google(audio)
            print(said)
        except Exception as e:
            print("Exception: " + str(e))
    return said.lower()

# WAKE = 'hi tom'
#
# while True:
#     _text = get_audio()
#     if WAKE in _text:
#         speak('Hello, how are you? What can I do for you?')
#     if 'bye' in _text:
#         speak('Bye')
#         time.sleep(1)
#         break

class VoiceAssistant(threading.Thread):
    stop = False
    def run(self):
        time.sleep(1)
        say('greeting')
        while True:
            if self.stop:
                say('bye')
                print('I am off')
                break
            print('I am ready')
            time.sleep(1)

if __name__ == '__main__':
    speak('Hello, how are you? What can I do for you?', 'sound_greeting.mp3')
    speak('Bye-bye?', 'sound_bye.mp3')
    speak('I could not understand you. Please say a waste type again to search.', 'sound_again.mp3')
    speak('Great. I am going to search for you.', 'sound_search.mp3')