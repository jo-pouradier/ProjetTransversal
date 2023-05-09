from flask import Flask,request,abort,render_template,Response
from flask_httpauth import HTTPBasicAuth
import serial 
import json


class FlaskServer:
    def __init__(self,sharedVariables=None, sharedFrame=None) :
        self.ser = serial.Serial('/dev/ttyACM0')#change this to the name of your port
        self.ser.flushInput()
        self.ser.baudrate = 115200
        self.app = Flask(__name__)
        self.auth = HTTPBasicAuth()
        # add index page
        self.app.add_url_rule('/', 'index', self.index)
         # add decoration to check auth
        self.auth.verify_password(self.verify_password)
        # add decoration to check ip address with allowed_ips
        #self.app.before_request(self.check_ip)
        self.sharedFrame = sharedFrame
        self.sharedVariables = sharedVariables
        self.app.add_url_rule('/livecam', 'livecam',self.auth.login_required(self.livecam))

        self.app.add_url_rule('/commandes', 'commandes',self.auth.login_required(self.commandes), methods=['POST'])
        

      

        self.allowed_ips = ['127.0.0.1','134.214.51.113','192.168.56.1','192.168.202.1','182.168.252.154','192.168.252.154']#ip des appereils que l'on autorise à se connecter au serveur

        self.users = {
            "optimus": "optimus",
        }
        self.commandes = {
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

    def verify_password(self, username, password):
        if username in self.users and self.users[username] == password:
            return username
        
    def check_ip(self):
        if request.remote_addr not in self.allowed_ips:
            abort(403)
    
    def index(self):
        return render_template('index.html')
    def genFrames(self):
        while True:
            frame = self.sharedFrame.getFrame()
            # print(image is not None)
            # get width and height of frame, where frame is bytes encoded image
            if frame is not None:
                yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            else:
                # generate empty frame
                frame = b''
                yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    def livecam(self):
        return Response(self.genFrames(),mimetype='multipart/x-mixed-replace; boundary=frame')
    def commandes(self):
        #put in the shared variable the command
        print(self.sharedVariables)
        data = request.get_json(force=True)
        print(data["key"])
        if data['key'] in self.commandes.keys():
            print(self.commandes[data['key']])
            self.ser.write(bytes(self.commandes[data['key']], 'utf8'))
            return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

        else : 
            print("stop")
            self.ser.write(bytes("stop\r", 'utf8'))
            return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 
    def run(self):
        self.app.run(host="0.0.0.0", debug=False)

