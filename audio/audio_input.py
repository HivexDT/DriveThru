import os
import pyaudio
from audio.microphone import MicrophoneStream

def recognize_speech():
    # print("[DEBUG] recognize_speech() called")
    from speech.speech_recognition import SpeechRecognizer
    recognizer = SpeechRecognizer()
    result = recognizer.recognize_from_microphone()
    # print(f"[DEBUG] recognize_speech() result: {result}")
    return result 