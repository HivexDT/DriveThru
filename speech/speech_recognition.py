import os
import pyaudio
from google.cloud import speech_v1p1beta1 as speech
from audio.microphone import MicrophoneStream
from utils.config import GOOGLE_APPLICATION_CREDENTIALS, LANGUAGE_CODE

AUDIO_ENCODING = speech.RecognitionConfig.AudioEncoding.LINEAR16
INPUT_DEVICE_INDEX = 1  # Set to your working mic index
CHUNK = 1024

# Get the default sample rate for the selected input device
p = pyaudio.PyAudio()
input_info = p.get_device_info_by_index(INPUT_DEVICE_INDEX)
DEFAULT_SAMPLE_RATE = int(input_info['defaultSampleRate'])
p.terminate()

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_APPLICATION_CREDENTIALS

class SpeechRecognizer:
    def __init__(self):
        self.client = speech.SpeechClient()

    def recognize_from_microphone(self, duration=5):
        """
        Record audio from the microphone for a fixed duration and send to Google Speech API.
        """
        # print(f"[DEBUG] Recording {duration} seconds from device {INPUT_DEVICE_INDEX} at {DEFAULT_SAMPLE_RATE}Hz...")
        frames = []
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=DEFAULT_SAMPLE_RATE,
                        input=True,
                        input_device_index=INPUT_DEVICE_INDEX,
                        frames_per_buffer=CHUNK)
        for _ in range(0, int(DEFAULT_SAMPLE_RATE / CHUNK * duration)):
            data = stream.read(CHUNK)
            frames.append(data)
        stream.stop_stream()
        stream.close()
        p.terminate()
        audio_content = b''.join(frames)
        # print(f"[DEBUG] Total recorded bytes: {len(audio_content)}")
        # Send to Google Speech API
        audio = speech.RecognitionAudio(content=audio_content)
        config = speech.RecognitionConfig(
            encoding=AUDIO_ENCODING,
            sample_rate_hertz=DEFAULT_SAMPLE_RATE,
            language_code=LANGUAGE_CODE,
        )
        try:
            response = self.client.recognize(config=config, audio=audio)
            for result in response.results:
                transcript = result.alternatives[0].transcript
                confidence = result.alternatives[0].confidence
                print(f"[DEBUG] Transcript: {transcript}, Confidence: {confidence}")
                if confidence > 0.3:
                    print(f"Transcript: {transcript}")
                    return transcript
                else:
                    print("Low confidence, retrying...")
                    return None
            print("[DEBUG] No results in response.")
        except Exception as e:
            print(f"[DEBUG] Exception during speech recognition: {e}")
        return None

    def recognize_streaming(self, duration=5):
        """
        Record audio for a fixed duration, then send it to the Google streaming API in chunks.
        This mimics the reliable logic of testmic.py but uses the streaming API.
        """
        print(f"[DEBUG] Streaming recording {duration} seconds from device {INPUT_DEVICE_INDEX} at {DEFAULT_SAMPLE_RATE}Hz...")
        frames = []
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=DEFAULT_SAMPLE_RATE,
                        input=True,
                        input_device_index=INPUT_DEVICE_INDEX,
                        frames_per_buffer=CHUNK)
        for _ in range(0, int(DEFAULT_SAMPLE_RATE / CHUNK * duration)):
            data = stream.read(CHUNK)
            frames.append(data)
        stream.stop_stream()
        stream.close()
        p.terminate()
        audio_content = b''.join(frames)
        # print(f"[DEBUG] Total recorded bytes (streaming): {len(audio_content)}")
        # Send to Google Streaming Speech API in chunks
        def audio_generator():
            for i in range(0, len(audio_content), CHUNK):
                chunk = audio_content[i:i+CHUNK]
                yield chunk
        config = speech.RecognitionConfig(
            encoding=AUDIO_ENCODING,
            sample_rate_hertz=DEFAULT_SAMPLE_RATE,
            language_code=LANGUAGE_CODE,
        )
        streaming_config = speech.StreamingRecognitionConfig(config=config, interim_results=False)
        try:
            requests = (
                speech.StreamingRecognizeRequest(audio_content=content)
                for content in audio_generator()
            )
            responses = self.client.streaming_recognize(streaming_config, requests)
            found_transcript = None
            for response in responses:
                print("[DEBUG] Received response from Google Speech API.")
                if not response.results:
                    print("[DEBUG] No results in response.")
                for result in response.results:
                    transcript = result.alternatives[0].transcript
                    confidence = result.alternatives[0].confidence
                    # print(f"[DEBUG] Transcript: {transcript}, Confidence: {confidence}")
                    if confidence > 0.3:
                        print(f"Transcript: {transcript}")
                        found_transcript = transcript
            if found_transcript:
                return found_transcript
            print("[DEBUG] No valid transcript found in streaming response.")
        except Exception as e:
            print(f"[DEBUG] Exception during streaming speech recognition: {e}")
        return None 