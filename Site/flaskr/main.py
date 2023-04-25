from flask import Flask,Response,render_template,request
import cv2,time
import numpy as np
import pyaudio
import keyboard 
import obstacle as obs
#from scipy.signal import butter, lfilter
app = Flask(__name__)

camera= cv2.VideoCapture(0)


FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 0

 
audio1 = pyaudio.PyAudio()
 
for i in range(audio1.get_device_count()):
    info = audio1.get_device_info_by_index(i)
    if info['maxInputChannels'] > 0:
        print(f"Index : {i}, Nom : {info['name']}")


def liveCam() :
    '''Live camera feed
    Description: this basic function will return the camera frame as a byte stream 
    Returns: the camera frame 
    '''

    while True:
        ## read the camera frame
        success,frame=camera.read()
        if not success:
            break
        else:
            ret,buffer=cv2.imencode('.jpg',frame)
            frame=buffer.tobytes()

        yield(b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def detectionV2() :
    '''Face detection
    Description: this function will return the camera frame with a rectangle around the face
    Returns: the camera frame with a rectangle around the face and numbers of face detected
    '''
    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    camera.set(3,640) # set Width
    camera.set(4,480) # set Height
    cv2.setUseOptimized(True)
    cv2.setNumThreads(1)

    FPS = 30
    timer = 1/FPS

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
        for (x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]  
        
        #text fps
        #fps = 1/(new_frame_time-prev_frame_time)
        prev_frame_time = new_frame_time
        new_frame_time = time.perf_counter()
        #cv2.putText(img, text=str(np.round(fps, 1)), org=(7, 70), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(0, 0, 0), thickness=2, lineType=cv2.LINE_AA)

        cv2.putText(img, text="nbr de face: " + str(len(faces)),org=(7, 70), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(0, 0, 0), thickness=2, lineType=cv2.LINE_AA)
        ret,buffer=cv2.imencode('.jpg',img)
        frame=buffer.tobytes()

        yield(b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def genHeader(sampleRate, bitsPerSample, channels):
    '''Generates a header
    Description: this function will return the header of the audio file
    Returns: the header of the audio file
    '''
    
    datasize = 2000*10**6
    o = bytes("RIFF",'ascii')                                               # (4byte) Marks file as RIFF
    o += (datasize + 36).to_bytes(4,'little')                               # (4byte) File size in bytes excluding this and RIFF marker
    o += bytes("WAVE",'ascii')                                              # (4byte) File type
    o += bytes("fmt ",'ascii')                                              # (4byte) Format Chunk Marker
    o += (16).to_bytes(4,'little')                                          # (4byte) Length of above format data
    o += (1).to_bytes(2,'little')                                           # (2byte) Format type (1 - PCM)
    o += (channels).to_bytes(2,'little')                                    # (2byte)
    o += (sampleRate).to_bytes(4,'little')                                  # (4byte)
    o += (sampleRate * channels * bitsPerSample // 8).to_bytes(4,'little')  # (4byte)
    o += (channels * bitsPerSample // 8).to_bytes(2,'little')               # (2byte)
    o += (bitsPerSample).to_bytes(2,'little')                               # (2byte)
    o += bytes("data",'ascii')                                              # (4byte) Data Chunk Marker
    o += (datasize).to_bytes(4,'little')                                    # (4byte) Data size in bytes
    return o


    ## Adaptez ces paramètres 
    CHANNELS = 1
    RATE = 16000
    high_cutoff = 1000
    low_cutoff = 200
    '''
    def butter_bandpass(data, high_cutoff,low_cutoff, fs, order=2):
        nyq = 0.4 * fs
        high = high_cutoff/nyq
        low = low_cutoff/nyq
        b,a = butter(order, [low, high], btype='bandpass', analog=False)
        y = lfilter(b,a,data)
        y = y.astype(np.int16)
        return y
    '''
    p = pyaudio.PyAudio()
    print('Starting audio...')
    stream_in = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK_SIZE,
                    input_device_index=0)

    stream_out = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        output=True,
                        frames_per_buffer=CHUNK_SIZE)

    while True:
        data = stream_in.read(CHUNK_SIZE)
        data_np = np.frombuffer(data,dtype=np.int16)
        input = data_np.astype(np.float32)

        #data_output = butter_bandpass(input, high_cutoff, low_cutoff, RATE)
        stream_out.write(input.tobytes())

        if keyboard.is_pressed('s'):
            print('End')
            break




# --------------------------------------------------------------------------------------------
# Routes
@app.route('/index')
def index():
    return render_template('index.html')

@app.route("/livecam")
def streamcam():
    return Response(detectionV2(),mimetype='multipart/x-mixed-replace; boundary=frame')

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
                        rate=RATE, input=True,input_device_index=1,
                        frames_per_buffer=CHUNK)
        print("recording...")
        #frames = []
        first_run = True
        while True:
           if first_run:
               data = wav_header + stream.read(CHUNK)
               first_run = False
           else:
               data = stream.read(CHUNK)
           yield(data)
    return Response(sound())



"""
partie du code pour piloter le robot à distance : quand on appuie sur une touche, on appelle 
une fonction qui transmet en langage uart l'opération voulue 
"""

@app.route('/appeler_fonction_avancer', methods=['POST'])
def appeler_fonction_avancer():
    # Appeler la fonction correspondante ici
    avancer()
    print("z")
    return ''

def avancer():
    print("On rentre dans la fonction avancer")
    return "mogo 1:20 2:20"







if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
    