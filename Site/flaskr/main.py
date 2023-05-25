import flask
import cv2
import serial 
from flask_httpauth import HTTPBasicAuth
import os
import json
import pyaudio
import imutils
import simpleaudio
import speech_to_text 



#ATTENTION : VERIFIER PORT + BAUD RATE
ser = serial.Serial('/dev/ttyACM0')#change this to the name of your port
ser.flushInput()
ser.baudrate = 115200 #change this to your actual baud rate

#Sécurité: autorise seulement certaine IP + demande un identifiant et un mot de passe
app = flask.Flask(__name__)
auth = HTTPBasicAuth()

camera= cv2.VideoCapture(0)

ser = serial.Serial('/dev/ttyACM0')#change this to the name of your port
ser.flushInput()
ser.baudrate = 115200


allowed_ips = ['192.168.119.187','134.214.51.113','134.214.51.81','192.168.56.1','192.168.202.1','192.168.252.254', '192.168.252.187','192.168.252.154', '192.168.252.32', '127.0.0.1']#ip des appereils que l'on autorise à se connecter au serveur

users = {
    "optimus": {
        "password": "optimus",
        "failed_attempts": 0,
    },
}
MAX_LOGIN_ATTEMPTS = 3

#Intialisation for keys:
COMMANDES = {
        'z' : 'avancerR\r',
        'q' : 'gaucheR\r',
        's' : 'arriereR\r',
        'd' : 'droiteR\r',
        ' ' : 'stop\r',
        'ArrowUp' : 'hautC\r',
        'ArrowDown' : 'basC\r',
        'ArrowLeft' : 'gaucheC\r',
        'ArrowRight' : 'droiteC\r',
        'Enter' : 'stop\r',
    }
 
@auth.verify_password
def verify_password(username, password):
     if username in users and users[username]["password"] == password:
         users[username]["failed_attempts"] = 0  # reset failed attempts on successful login
         return username
     elif username in users:
         users[username]["failed_attempts"] += 1
         if users[username]["failed_attempts"] >= MAX_LOGIN_ATTEMPTS:
             del users[username]  # block the user after max attempts
             return "blocked"
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


def detection() :
        front_face_path = os.path.join(os.path.dirname(__file__), 'haarcascade_frontalface_default.xml')
        cam_config = {
            "compteur" : 0,
            "anglex" : 0,
            "angley" : 0,
            "FPS" : 8,
            "WIDTH" : 200,
            "HEIGHT" : 200,
            "faceCascade" : cv2.CascadeClassifier(front_face_path)
        }

        cam_config["Screenmiddle"] = (cam_config["WIDTH"]//2,cam_config["HEIGHT"]//2)
        cam_config["RapportConvx"] = (2/cam_config["WIDTH"])
        cam_config["RapportConvy"] = (2/cam_config["HEIGHT"])
        
        #Implementing our parameters
        camera.set(cv2.CAP_PROP_FRAME_WIDTH,cam_config["WIDTH"]) 
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT,cam_config["HEIGHT"])
        camera.set(cv2.CAP_PROP_FPS,cam_config["FPS"])

        while True:
            #Local variables
            airemax=0
            Centreproche=0
            AxeX=0
            AxeY=0


            # Capture frame-by-frame
            ret, frame = camera.read()
            # Our operations on the frame come hereq
            #alphachannel = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)       
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Create the haar cascade
            
            # Detect faces in the image
            faces = cam_config["faceCascade"].detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30)
            )
            
            
            # Draw a rectangle around the faces
            for (x, y, w, h) in faces:
                
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 255, 255), 2)
                #Calcul the area of the rectangle
                airelocale=int(abs(x+w-x)*abs(y+h-y))
                #Only keeping in memory the largest recangle
                
                
                if airelocale>=airemax:
                    airemax=airelocale
                    #Converting the pixel-distance  pixel in angular distance for the servo motor
                    Centreproche=((x+x+w)/2,(y+h+y)/2)

                    cam_config["anglex"]=(Centreproche[0]-cam_config["Screenmiddle"][0])
                    cam_config["angley"]=(Centreproche[1]-cam_config["Screenmiddle"][1])
                
                
                if (Centreproche[0]>20 and Centreproche[0]<cam_config["WIDTH"]-20):
                    if cam_config["anglex"]>10:
                        AxeX=-1
                    elif cam_config["anglex"]<-10:
                        AxeX=1
                if (Centreproche[1]>20 and Centreproche[1]<cam_config["HEIGHT"]-20):
                    if cam_config["angley"]>5:
                        AxeY=1
                    elif cam_config["angley"]<-5:
                        AxeY=-1

            #Printing the number of face found
            print ("Found {0} faces!".format(len(faces)))

            if AxeX==1:
                ser.write(bytes("droiteC\r",'utf8'))
                print("droite")
            elif AxeX==-1:
                ser.write(bytes("gaucheC\r",'utf8'))   
                print("gauche")      
            if AxeY==1:
                ser.write(bytes("basC\r",'utf8'))
                print("bas")
            elif AxeY==-1:
                ser.write(bytes("hautC\r",'utf8'))
                print("haut")
    
            cam_config["compteur"]+=1
            frame_resize = imutils.resize(frame , height=200)
            frame_resize = imutils.resize(frame , width=200)
            ret,buffer=cv2.imencode('.jpg',frame_resize)
            frame=buffer.tobytes()
            yield(b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break


def genHeader(sampleRate, bitsPerSample, channels):
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

def rec_sound():
        p = pyaudio.PyAudio()
        print('first sound')
        CHUNK_SIZE = 1024
        FORMAT = pyaudio.paInt16
        ## Adaptez ces paramètres 
        CHANNELS = 2
        RATE = 44100
        
        # p = pyaudio.PyAudio()
        print("start")
        bitsPerSample = 16
        channels = 2
        wav_header = genHeader(RATE, bitsPerSample, channels)
        stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK_SIZE)
        data = wav_header + stream.read(CHUNK_SIZE)
        while True:
               data += stream.read(CHUNK_SIZE)
               yield(data)
               

        

# --------------------------------------------------------------------------------------------
# Routes
@check_ip
@app.route('/', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'POST':
        username = flask.request.form['username']
        password = flask.request.form['password']
        result = verify_password(username, password)
        if result == "blocked":
            return flask.render_template('login.html', error="Too many failed login attempts. You are blocked.")
        elif result:
            return flask.render_template('index.html')
        else:
            if username in users:
                failed_attempts = users[username]["failed_attempts"]
                if failed_attempts >= MAX_LOGIN_ATTEMPTS - 1:
                    return flask.render_template('login.html', error="Invalid username or password. This is your last attempt.")
            return flask.render_template('login.html', error="Invalid username or password")
    return flask.render_template('login.html')


@app.route("/livecam")
def livecam():
    return flask.Response(detection(),mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/commandes', methods=['POST'])
def deplacements():
    sp = speech_to_text.SpeechRecognition()
    get_key = flask.request.get_json(force=True)

    # gestion du mode automatique
    if get_key['key'] == 'a':
        print("mode automatique")

    if get_key['key'] in COMMANDES.keys():
        ser.write(bytes(COMMANDES[get_key['key']], 'utf8'))
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 
    if get_key['key'] == 'k':
        sp.play_motDoux2("joie")
    if get_key['key'] == 'l':
        sp.play_motDoux2("tristesse")
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 


@app.route('/protected')
def protected_route():
    return  "Vous êtes connecté en tant que : {} et votre adresse IP est autorisée.".format(auth.current_user())


@app.route("/audio_stream")
def audio_stream():
    print("coucou")
    return flask.Response(rec_sound(),mimetype='audio/x-wav; codec=pcm')

def main():
    app.run(host='0.0.0.0', port=5001)

if __name__ == '__main__':
    main()


