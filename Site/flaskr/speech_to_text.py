import speech_recognition as sr
import pyaudio
import wave
# import math
# import unidecode
class SpeechRecognition:

    def __init__(self):
        self.text = ''
        self.listJoie = ["joie"]
        self.listColere = ["colère"]
        self.listTristesse = ["tristesse"]


    def continuous_speech_to_text(self, audio_bytes):
        # Create a recognizer object
        r = sr.Recognizer()

        # Use the default microphone as the audio source
        with sr.AudioFile(audio_bytes) as source:
            # Adjust for ambient noise
            r.adjust_for_ambient_noise(source)

            # Continuously listen for speech and convert it to text
            while True:
                try:
                    print("Say something:")
                    audio = r.listen(source)
                    self.text += r.recognize_google(audio, language="fr-FR")
                    print(self.text)
                    self.analyze_text()
                except sr.UnknownValueError:
                    print("Could not understand audio")
                except sr.RequestError as e:
                    print("Could not request results from Google Speech Recognition service; {0}".format(e))


    def analyze_text(self):
        if self.text != '':
            list = []
            list = self.text.split(" ")
            for i in list:
                print(i)
                if i in self.listJoie:
                    self.play_motDoux("joie")
                elif i in self.listColere:
                    self.play_motDoux("colere")
                elif i in self.listTristesse:
                    self.play_motDoux("tristesse")
                else:
                    pass
        else:
            pass

    def play_motDoux(self, emotion):
        # play the file selected
        file = self.select_motDoux(emotion)
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


    def select_motDoux(self, emotion):
        # return a file depending on the emotion entered
        #r = math.random.randint(1, 10) # le 10 dépend du nombre de fichiers audio dans le dossier
        #return f"audio/{emotion}/{emotion}{r}.wav"
        return f"../../son/audio/{emotion}/{emotion}.wav"


if __name__ == "__main__":
    a = SpeechRecognition()
    a.continuous_speech_to_text()
