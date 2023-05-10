import flask
import cv2
import time
import numpy as np
import pyaudio
import serial
import keyboard
import obstacle as obs
from flask_httpauth import HTTPBasicAuth
import time
import speech_to_text as stt
# from scipy.signal import butter, lfilter


# ATTENTION : VERIFIER PORT + BAUD RATE
# ser = serial.Serial('/dev/ttyACM0')  # change this to the name of your port
# ser.flushInput()
# ser.baudrate = 115200  # change this to your actual baud rate

# Sécurité : autorise seulement certaine IP + demande un identifiant et un mot de passe
auth = HTTPBasicAuth()

allowed_ips = ['134.214.51.81', '192.168.56.1', '192.168.202.1', '192.168.252.254', '192.168.252.187',
               '192.168.252.32', '127.0.0.1']  # ip des appareils que l'on autorise à se connecter au serveur

users = {
    "optimus": {
        "password": "optimus",
        "failed_attempts": 0,
    },
}
MAX_LOGIN_ATTEMPTS = 3


@auth.verify_password
def verify_password(username, password):
    if username in users and users[username]["password"] == password:
        users[username]["failed_attempts"] = 0  # reset failed attempts on successful login
        return username
    elif username in users:
        users[username]["failed_attempts"] += 1
        if users[username]["failed_attempts"] >= MAX_LOGIN_ATTEMPTS:
            del users[username]  # block the user after max attempts
        return None
    else:
        return None


def check_ip(f):
    def wrapped(*args, **kwargs):
        client_ip = flask.request.remote_addr
        if client_ip not in allowed_ips:
            flask.abort(403)  # Forbidden
        return f(*args, **kwargs)

    return wrapped


# from scipy.signal import butter, lfilter
app = flask.Flask(__name__)

camera = cv2.VideoCapture(0)

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 0

# Intialisation for keys:
CONFIG = {

}
COMMANDES: dict = {
    'z': 'avancerR\r',
    'q': 'gaucheR\r',
    's': 'arriereR\r',
    'd': 'droiteR\r',
    ' ': 'stop\r',
    'ArrowUp': 'hautC\r',
    'ArrowDown': 'basC\r',
    'ArrowLeft': 'gaucheC\r',
    'ArrowRight': 'droiteC\r',
    'Enter': 'stop\r',
}

audio1 = pyaudio.PyAudio()

for i in range(audio1.get_device_count()):
    info = audio1.get_device_info_by_index(i)
    if info['maxInputChannels'] > 0:
        print(f"Index : {i}, Nom : {info['name']}")


def liveCam():
    '''Live camera feed
    Description: this basic function will return the camera frame as a byte stream 
    Returns: the camera frame 
    '''

    while True:
        # read the camera frame
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


def detectionV2():
    '''Face detection
    Description: this function will return the camera frame with a rectangle around the face
    Returns: the camera frame with a rectangle around the face and numbers of face detected
    '''
    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    camera.set(3, 640)  # set Width
    camera.set(4, 480)  # set Height
    cv2.setUseOptimized(True)
    cv2.setNumThreads(1)

    FPS = 30
    timer = 1 / FPS

    prev_frame_time = 0
    new_frame_time = 1

    while True:

        ret, img = camera.read()
        # filp image horizontaly like mirror
        img = cv2.flip(img, 1)
        # waiting fps
        if new_frame_time - prev_frame_time < timer:
            time.sleep(timer - (new_frame_time - prev_frame_time))

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Detect faces in the image
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(20, 20)
        )
        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = img[y:y + h, x:x + w]

            # text fps
        # fps = 1/(new_frame_time-prev_frame_time)
        prev_frame_time = new_frame_time
        new_frame_time = time.perf_counter()
        # cv2.putText(img, text=str(np.round(fps, 1)), org=(7, 70), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(0, 0, 0), thickness=2, lineType=cv2.LINE_AA)

        cv2.putText(img, text="nbr de face: " + str(len(faces)), org=(7, 70), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=1, color=(0, 0, 0), thickness=2, lineType=cv2.LINE_AA)
        ret, buffer = cv2.imencode('.jpg', img)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


def genHeader(sampleRate, bitsPerSample, channels):
    '''Generates a header
    Description: this function will return the header of the audio file
    Returns: the header of the audio file
    '''

    datasize = 2000 * 10 ** 6
    o = bytes("RIFF", 'ascii')  # (4byte) Marks file as RIFF
    o += (datasize + 36).to_bytes(4, 'little')  # (4byte) File size in bytes excluding this and RIFF marker
    o += bytes("WAVE", 'ascii')  # (4byte) File type
    o += bytes("fmt ", 'ascii')  # (4byte) Format Chunk Marker
    o += (16).to_bytes(4, 'little')  # (4byte) Length of above format data
    o += (1).to_bytes(2, 'little')  # (2byte) Format type (1 - PCM)
    o += channels.to_bytes(2, 'little')  # (2byte)
    o += sampleRate.to_bytes(4, 'little')  # (4byte)
    o += (sampleRate * channels * bitsPerSample // 8).to_bytes(4, 'little')  # (4byte)
    o += (channels * bitsPerSample // 8).to_bytes(2, 'little')  # (2byte)
    o += bitsPerSample.to_bytes(2, 'little')  # (2byte)
    o += bytes("data", 'ascii')  # (4byte) Data Chunk Marker
    o += datasize.to_bytes(4, 'little')  # (4byte) Data size in bytes
    return o


# --------------------------------------------------------------------------------------------
# Routes
@app.route('/index')
@auth.login_required
@check_ip
def index():
    return flask.render_template('index.html')


@app.route("/livecam")
def streamcam():
    return flask.Response(detectionV2(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route("/recordNplay")
def playSounds():
    def sound():
        ### IL FAUT ADAPTER CES PARAM AU PARAM DE VOTRE MICRO ###
        sampleRate = 44100
        bitsPerSample = 16
        channels = 1
        #########################################################

        wav_header = genHeader(sampleRate, bitsPerSample, channels)

        stream = audio1.open(format=FORMAT, channels=CHANNELS,
                             rate=RATE, input=True, input_device_index=1,
                             frames_per_buffer=CHUNK)
        print("recording...")
        # frames = []
        first_run = True
        while True:
            if first_run:
                data = wav_header + stream.read(CHUNK)
                first_run = False
            else:
                data = stream.read(CHUNK)
            yield data

    a = stt.speechRecognition()
    a.continuous_speech_to_text(sound())
    return flask.Response(sound())


"""
partie du code pour piloter le robot à distance : quand on appuie sur une touche, on appelle 
une fonction qui transmet en langage uart l'opération voulue 
"""


# Initialisation :
# global get_key
# get_key = ""
@app.route('/deplacements', methods=['POST'])
def deplacements():
    get_key = flask.request.get_json(force=True)
    # gestion du mode automatique
    if get_key['key'] == 'a':
        print("mode automatique")

    if get_key['key'] in COMMANDES.keys():
        ser.write(bytes(COMMANDES[get_key['key']], 'utf8'))
        return 200
    # CONFIG["last_get_key"] = get_key
    return 400


@app.route('/stop', methods=['POST'])
def stop():
    ser.write(bytes("stop", 'utf8'))
    return ""


@app.route('/protected')
def protected_route():
    return "Vous êtes connecté en tant que : {} et votre adresse IP est autorisée.".format(auth.current_user())


def testFast(x):
    y = 0
    for i in range(0, x):
        y *= i
    return y


def main():
    app.run(host='0.0.0.0', port=5001)


if __name__ == '__main__':
    main()
