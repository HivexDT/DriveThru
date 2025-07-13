import pyaudio

p = pyaudio.PyAudio()
print("Connected and working audio devices:")

for i in range(p.get_device_count()):
    info = p.get_device_info_by_index(i)
    name = info['name']
    max_input = info['maxInputChannels']
    max_output = info['maxOutputChannels']
    is_working = False

    # Check for input device
    if max_input > 0:
        try:
            stream = p.open(format=pyaudio.paInt16,
                            channels=1,
                            rate=int(info['defaultSampleRate']),
                            input=True,
                            input_device_index=i)
            stream.close()
            is_working = True
        except Exception as e:
            pass  # Device not available for input

    # Check for output device
    if max_output > 0:
        try:
            stream = p.open(format=pyaudio.paInt16,
                            channels=1,
                            rate=int(info['defaultSampleRate']),
                            output=True,
                            output_device_index=i)
            stream.close()
            is_working = True
        except Exception as e:
            pass  # Device not available for output

    if is_working:
        print(f"Device {i}: {name} (Input: {max_input}, Output: {max_output}) [WORKING]")
    else:
        print(f"Device {i}: {name} (Input: {max_input}, Output: {max_output}) [NOT WORKING]")

p.terminate()