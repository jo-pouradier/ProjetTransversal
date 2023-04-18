
import pyaudio
import numpy as np
'''
# Define the frequency and duration of the tone
frequency = 550 # Hz
duration = 10 # seconds

# Initialize PyAudio
p = pyaudio.PyAudio()

# Generate the audio data
sampling_rate = 44100 # Hz
t = np.linspace(0, duration, int(sampling_rate * duration), False)
audio_data = np.sin(2 * np.pi * frequency * t).astype(np.float32)

# Open a new stream for output
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=sampling_rate,
                output=True)

# Play the audio data
stream.write(audio_data)

# Close the stream and PyAudio
stream.stop_stream()
stream.close()
p.terminate()
'''
pa = pyaudio.Pyaudio()

for i in range(pa.get_device_count()):
    info = pa.get_device_info_by_index(i)
    if info['maxInputChannels'] > 0:
        print(f"Index : {i}, Nom : {info['name']}")