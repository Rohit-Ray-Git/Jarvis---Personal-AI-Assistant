# tts.py
# Placeholder for text-to-speech logic using Edge-TTS 

import pyttsx3

def speak_text(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 180)  # Adjust speaking rate if desired
    engine.say(text)
    engine.runAndWait() 