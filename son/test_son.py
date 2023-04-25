
import pyaudio
import numpy as np
import math

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

def select_motDoux(emotion):
    # return a file depending on the emotion entered
    if emotion == "joie":
        r = math.random.randint(0, 10) # le 10 dépend du nombre de fichiers audio dans le dossier
        return f"audio/joie/joie{r}.wav"
    elif emotion == "tristesse":
        r = math.random.randint(0, 10)
        return f"audio/tristesse/tristesse{r}.wav"
    elif emotion == "colere":
        r = math.random.randint(0, 10)
        return f"audio/colere/colere{r}.wav"
    
def play_motDoux(emotion):
    # play the file selected
    file = select_motDoux(emotion)
    chunk = 1024
    wf = wave.open(file, 'rb')
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
    data = wf.readframes(chunk)
    while data != b'':
        stream.write(data)
        data = wf.readframes(chunk)
    stream.stop_stream()
    stream.close()
    p.terminate()


