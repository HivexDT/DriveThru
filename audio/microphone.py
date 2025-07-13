import io
import pyaudio

class MicrophoneStream:
    def __init__(self, rate, chunk, input_device_index=None):
        self._rate = rate
        self._chunk = chunk
        self._buff = io.BytesIO()
        self._audio_interface = None
        self._audio_stream = None
        self.closed = True
        self.input_device_index = input_device_index

    def __enter__(self):
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self._rate,
            input=True,
            input_device_index=self.input_device_index,
            frames_per_buffer=self._chunk,
            stream_callback=self._fill_buffer,
        )
        print("[DEBUG] Audio stream started.")
        self.closed = False
        return self

    def __exit__(self, type, value, traceback):
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        print("[DEBUG] Audio stream stopped.")
        self.closed = True
        self._buff.seek(0)
        self._buff.write(b"")
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        print(f"[DEBUG] Captured audio chunk of size: {len(in_data)} bytes")
        self._buff.write(in_data)
        # Optionally, save the raw audio to a file for debugging
        with open("debug_last_chunk.raw", "wb") as f:
            f.write(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        while not self.closed:
            chunk = self._buff.read(self._chunk)
            print(f"[DEBUG] Yielding audio chunk of size: {len(chunk) if chunk else 0} bytes")
            if chunk:
                # Save chunk for debugging
                with open("debug_last_yielded_chunk.raw", "wb") as f:
                    f.write(chunk)
            if not chunk:
                print("[DEBUG] No chunk to yield, breaking generator loop.")
                return
            yield chunk 