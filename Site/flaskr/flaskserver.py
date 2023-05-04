from flask import Flask,request,abort,render_template,Response
from flask_httpauth import HTTPBasicAuth

class FlaskServer:
    def __init__(self,sharedVariables=None, sharedFrame=None) :
        self.app = Flask(__name__)
        self.auth = HTTPBasicAuth()
        # add index page
        self.app.add_url_rule('/', 'index', self.index)
         # add decoration to check auth
        self.auth.verify_password(self.verify_password)
        # add decoration to check ip address with allowed_ips
        #self.app.before_request(self.check_ip)
        self.app.add_url_rule('/livecam', 'livecam', self.livecam)
        self.sharedFrame = sharedFrame

      

        self.allowed_ips = ['127.0.0.1','134.214.51.113','192.168.56.1','192.168.202.1','182.168.252.154']#ip des appereils que l'on autorise à se connecter au serveur

        self.users = {
            "optimus": "optimus",
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
        return self.commandes.run()
    
    def run(self):
        self.app.run(host="0.0.0.0", debug=False)
