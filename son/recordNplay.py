import pyaudio
import keyboard 
from scipy.signal import butter, lfilter
import numpy as np

CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16

## Adaptez ces paramètres 
CHANNELS = 1
RATE = 44100
high_cutoff = 1000
low_cutoff = 200
def butter_bandpass(data, high_cutoff,low_cutoff, fs, order=2):
    nyq = 0.4 * fs
    high = high_cutoff/nyq
    low = low_cutoff/nyq
    b,a = butter(order, [low, high], btype='bandpass', analog=False)
    y = lfilter(b,a,data)
    y = y.astype(np.int16)
    return y

p = pyaudio.PyAudio()
print('Starting audio...')
stream_in = p.open(format=FORMAT,
                   channels=CHANNELS,
                   rate=RATE,
                   input=True,
                   frames_per_buffer=CHUNK_SIZE)

stream_out = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    output=True,
                    frames_per_buffer=CHUNK_SIZE)

while True:
    data = stream_in.read(CHUNK_SIZE)
    data_np = np.frombuffer(data,dtype=np.int16)
    input = data_np.astype(np.float32)

    data_output = butter_bandpass(input, high_cutoff, low_cutoff, RATE)
    stream_out.write(data_output.tobytes())
    #stream_in.read(CHUNK_SIZE)
    if keyboard.is_pressed('s'):
        print('End')
        break