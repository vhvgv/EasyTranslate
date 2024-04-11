import concurrent.futures
import requests
import re
import os
import html
import urllib.parse
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound

class EasyGoogleTranslate:
    def __init__(self, target_language='tr', timeout=5):
        self.target_language = target_language
        self.timeout = timeout
        self.pattern = r'(?s)class="(?:t0|result-container)">(.*?)<'

    def make_request(self, target_language, text, timeout):
        escaped_text = urllib.parse.quote(text.encode('utf8'))
        url = 'https://translate.google.com/m?tl=%s&q=%s' % (target_language, escaped_text)
        response = requests.get(url, timeout=timeout)
        result = response.text.encode('utf8').decode('utf8')
        result = re.findall(self.pattern, result)
        if not result:
            print('\nError: Unknown error.')
            f = open('error.txt')
            f.write(response.text)
            f.close()
            exit(0)
        return html.unescape(result[0])

    def translate(self, text, target_language='', timeout=''):
        if not target_language:
            target_language = self.target_language
        if not timeout:
            timeout = self.timeout
        if len(text) > 5000:
            print('\nError: It can only detect 5000 characters at once. (%d characters found.)' % (len(text)))
            exit(0)
        return self.make_request(target_language, text, timeout)

def get_language_options():
    print("Enter the target language code (e.g., 'en' for English):")
    target_language = input()
    return target_language

def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Please speak:")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        print("You said:", text)
        return text
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))

def text_to_speech(text, language='en'):
    tts = gTTS(text=text, lang=language, slow=False)
    tts.save("output.mp3")
    playsound("output.mp3")

if __name__ == "__main__":
    target_language = get_language_options()
    translator = EasyGoogleTranslate(target_language=target_language)

    # Get input from speech
    text = speech_to_text()

    # Check if speech recognition was successful
    if text is not None:
        # Translate the text
        translated_text = translator.translate(text)
        print("Translated text:", translated_text)

        # Convert translated text to speech
        text_to_speech(translated_text, target_language)
    else:
        print("Speech recognition failed. Please try again.")
