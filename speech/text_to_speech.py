import os
import time
from google.cloud import texttospeech
from utils.config import GOOGLE_APPLICATION_CREDENTIALS, LANGUAGE_CODE

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_APPLICATION_CREDENTIALS
text_to_speech_client = texttospeech.TextToSpeechClient()

def synthesize_speech(text, output_filename=None):
    if output_filename is None:
        output_filename = f"output_{int(time.time() * 1000)}.mp3"
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code=LANGUAGE_CODE, ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
    response = text_to_speech_client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    with open(output_filename, "wb") as out:
        out.write(response.audio_content)
        print(f'Audio content written to file "{output_filename}"')
    return output_filename 