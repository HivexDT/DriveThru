import time
import os
from utils.config import GOOGLE_APPLICATION_CREDENTIALS, PROJECT_ID, DIALOGFLOW_AGENT, LOCATION, LANGUAGE_CODE
from audio.audio_input import recognize_speech
from audio.audio_output import play_audio
from speech.speech_recognition import SpeechRecognizer
from speech.text_to_speech import synthesize_speech
from nlu.dialogflow_client import detect_intent_texts
from logic.order_logic import handle_order


def main():
    print("Drive-Thru System Started!")
    fulfillment_text = "Welcome to Student Burger drive-through.  What can I get for you today?"
    audio_file = synthesize_speech(fulfillment_text)
    play_audio(audio_file)
    if os.path.exists(audio_file):
        os.remove(audio_file)
    time.sleep(1)
    while True:
        print("Listening...")
        transcript = recognize_speech()
        if transcript:
            fulfillment_text, intent, parameters = detect_intent_texts(transcript)
            print(f"Dialogflow Intent: {intent}")
            print(f"Fulfillment Text: {fulfillment_text}")
            response = handle_order(intent, parameters)
            audio_file = synthesize_speech(response)
            play_audio(audio_file)
            if os.path.exists(audio_file):
                os.remove(audio_file)
            if intent == "CompleteOrder":
                break
            time.sleep(1)
        else:
            print("No speech detected. Please try again.")
            fulfillment_text = "Sorry, I didn't hear anything.  Could you repeat your order?"
            audio_file = synthesize_speech(fulfillment_text)
            play_audio(audio_file)
            if os.path.exists(audio_file):
                os.remove(audio_file)
            time.sleep(1)

if __name__ == "__main__":
    main() 