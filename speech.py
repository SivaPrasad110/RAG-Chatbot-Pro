"""
speech.py
Voice Input & Text to Speech
"""

import speech_recognition as sr
import pyttsx3

# ---------------------------------------
# Initialize TTS Engine
# ---------------------------------------

engine = pyttsx3.init()

engine.setProperty("rate", 170)

voices = engine.getProperty("voices")

if voices:
    engine.setProperty("voice", voices[0].id)


# ---------------------------------------
# Text To Speech
# ---------------------------------------

def speak(text):

    try:

        engine.say(text)

        engine.runAndWait()

    except Exception as e:

        print(e)


# ---------------------------------------
# Voice Input
# ---------------------------------------

def listen():

    recognizer = sr.Recognizer()

    with sr.Microphone() as source:

        print("Listening...")

        recognizer.adjust_for_ambient_noise(source)

        audio = recognizer.listen(source)

    try:

        text = recognizer.recognize_google(audio)

        return text

    except sr.UnknownValueError:

        return ""

    except Exception:

        return ""