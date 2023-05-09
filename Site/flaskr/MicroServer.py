import pyaudio
from flask import Flask, app, render_template
from flask_socketio import SocketIO
import socketio 
import  speech_to_text as stt

class MicroServer():
    def __init__(self, sharedVariables=None, sharedFrame=None):

        self.sharedVariables = sharedVariables
        self.sharedFrame = sharedFrame

        # self.sampleRate = 44100
        # self.bitsPerSample = 16
        # self.channels = 1
        # self.app = Flask(__name__)
        # self.recognizer = stt.SpeechRecognition()
        
        # #self.app.config['SECRET_KEY'] = 'secret!'
        # self.socketio = SocketIO(self.app)
        # self.format = pyaudio.paInt16
        # self.chunk = 1024
        
        # self.p = pyaudio.PyAudio()
        # self.stream = self.p.open(format=self.format,
        #         channels=self.channels,
        #         rate=self.sampleRate,
        #         input=True,
        #         frames_per_buffer=self.chunk)

    # @socketio.on('audio')
    def handle_audio(data):
         stt.continuous_speech_to_text(data)

    # @socketio.on('connect')
    # def handle_connect():
    #     print('Client connected')

    # @socketio.on('disconnect')
    # def handle_disconnect():
    #     print('Client disconnected')

    # @app.route('/')
    # def index():
    #     return render_template('index.html')

    def run(self):
        self.handle_audio(self.sharedVariables['audio'])
