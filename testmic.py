import pyaudio
import wave

p = pyaudio.PyAudio()
working_inputs = []
working_outputs = []

print("Connected and working input devices (microphones):")
for i in range(p.get_device_count()):
    info = p.get_device_info_by_index(i)
    name = info['name']
    max_input = info['maxInputChannels']
    if max_input > 0:
        try:
            stream = p.open(format=pyaudio.paInt16,
                            channels=1,
                            rate=int(info['defaultSampleRate']),
                            input=True,
                            input_device_index=i)
            stream.close()
            print(f"Device {i}: {name} (Input: {max_input}) [WORKING]")
            working_inputs.append((i, name, max_input, int(info['defaultSampleRate'])))
        except Exception:
            pass

print("\nConnected and working output devices (speakers/headphones):")
for i in range(p.get_device_count()):
    info = p.get_device_info_by_index(i)
    name = info['name']
    max_output = info['maxOutputChannels']
    if max_output > 0:
        try:
            stream = p.open(format=pyaudio.paInt16,
                            channels=1,
                            rate=int(info['defaultSampleRate']),
                            output=True,
                            output_device_index=i)
            stream.close()
            print(f"Device {i}: {name} (Output: {max_output}) [WORKING]")
            working_outputs.append((i, name, max_output, int(info['defaultSampleRate'])))
        except Exception:
            pass

if not working_inputs:
    print("No working microphones found.")
    p.terminate()
    exit()
if not working_outputs:
    print("No working speakers/headphones found.")
    p.terminate()
    exit()

# Select input device
if len(working_inputs) == 1:
    input_index = working_inputs[0][0]
    input_rate = working_inputs[0][3]
    print(f"Automatically selected input device {input_index}: {working_inputs[0][1]}")
else:
    input_index = int(input("Enter the device index for the microphone: "))
    input_rate = int(p.get_device_info_by_index(input_index)['defaultSampleRate'])

# Select output device
if len(working_outputs) == 1:
    output_index = working_outputs[0][0]
    output_rate = working_outputs[0][3]
    print(f"Automatically selected output device {output_index}: {working_outputs[0][1]}")
else:
    output_index = int(input("Enter the device index for the speaker/headphones: "))
    output_rate = int(p.get_device_info_by_index(output_index)['defaultSampleRate'])

# Use the lower of the two rates for compatibility
rate = min(input_rate, output_rate)
duration = 5  # seconds
frames = []
chunk = 1024

print(f"\nRecording 5 seconds from device {input_index}... Speak now!")
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=rate,
                input=True,
                input_device_index=input_index,
                frames_per_buffer=chunk)

for _ in range(0, int(rate / chunk * duration)):
    data = stream.read(chunk)
    frames.append(data)

stream.stop_stream()
stream.close()

# Save to file
wf = wave.open("mic_test.wav", "wb")
wf.setnchannels(1)
wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
wf.setframerate(rate)
wf.writeframes(b''.join(frames))
wf.close()

print("Recording saved as mic_test.wav.")

# Playback
print(f"Playing back through device {output_index}...")
wf = wave.open("mic_test.wav", "rb")
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=rate,
                output=True,
                output_device_index=output_index)

data = wf.readframes(chunk)
while data:
    stream.write(data)
    data = wf.readframes(chunk)

stream.stop_stream()
stream.close()
wf.close()
p.terminate()

print("Playback finished.")