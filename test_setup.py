import os
from utils import config
from google.cloud import speech
from google.cloud import dialogflow
from google.cloud import texttospeech



def test_credentials_file():
    path = config.GOOGLE_APPLICATION_CREDENTIALS
    exists = os.path.isfile(path)
    
      # Set the environment variable explicitly
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = config.GOOGLE_APPLICATION_CREDENTIALS
    print(f"Set GOOGLE_APPLICATION_CREDENTIALS to: {config.GOOGLE_APPLICATION_CREDENTIALS}")

    print(f"Credentials file exists: {exists} ({path})")
    return exists


def test_config_values():
    print(f"PROJECT_ID: {config.PROJECT_ID}")
    print(f"DIALOGFLOW_AGENT: {config.DIALOGFLOW_AGENT}")
    print(f"LOCATION: {config.LOCATION}")
    print(f"LANGUAGE_CODE: {config.LANGUAGE_CODE}")
    # Add more checks as needed
    return all([
        bool(config.PROJECT_ID),
        bool(config.DIALOGFLOW_AGENT),
        bool(config.LOCATION),
        bool(config.LANGUAGE_CODE),
    ])


def run_all_tests():
    print("Testing setup...")
    cred_ok = test_credentials_file()
    config_ok = test_config_values()
    if cred_ok and config_ok:
        print("Setup test PASSED.")
    else:
        print("Setup test FAILED.")

    # Test connections to Google APIs
    print("\nTesting Google Cloud API connections...")
    try:
        from google.cloud import speech
        from google.cloud import dialogflow
        from google.cloud import texttospeech
        speech_client = speech.SpeechClient()
        print("✓ Speech-to-Text API connected")
        dialogflow_client = dialogflow.SessionsClient()
        print("✓ Dialogflow API connected")
        tts_client = texttospeech.TextToSpeechClient()
        print("✓ Text-to-Speech API connected")
        print("\nAll APIs are working! You're ready to go!")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    run_all_tests() 