import pyaudio
import wave
import keyboard

CHUNK = 1024  # taille des données audio
FORMAT = pyaudio.paInt16  # format des données audio (16 bits)
CHANNELS = 1  # nombre de canaux (stéréo)
RATE = 16000  # fréquence d'échantillonnage (16 skHz)
WAVE_OUTPUT_FILENAME = "enregistrement.wav"  # nom du fichiers


p = pyaudio.PyAudio()
print('Début enregistrement')
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

frames = []

while True:
    data = stream.read(CHUNK)
    frames.append(data)
    
    if keyboard.is_pressed('s'):
        print('Fin enregistrement')
        break

    # écrire les données audio dans le fichier en temps réel
    with wave.open(WAVE_OUTPUT_FILENAME, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
    


stream.stop_stream()
stream.close()
p.terminate()
