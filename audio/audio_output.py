from pydub import AudioSegment
from pydub.playback import play
import playsound
import pyaudio
import wave

def play_audio(filename):
    try:
        sound = AudioSegment.from_mp3(filename)
        play(sound)
    except Exception as e:
        print(f"Error playing audio with pydub: {e}, trying playsound...")
        try:
            playsound.playsound(filename)
        except Exception as e2:
            print(f"Error playing audio with playsound: {e2}")

def play_audio_pyaudio(filename, output_device_index=None):
    wf = wave.open(filename, 'rb')
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True,
                    output_device_index=output_device_index)
    chunk = 1024
    data = wf.readframes(chunk)
    while data:
        stream.write(data)
        data = wf.readframes(chunk)
    stream.stop_stream()
    stream.close()
    p.terminate()
    wf.close() 