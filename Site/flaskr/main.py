from flask import Flask,Response,render_template
import cv2
app = Flask(__name__)

camera= cv2.VideoCapture(0)

def liveCam() :
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
    while(True):
        # Capture frame-by-frame
        ret, frame = camera.read()
        # Our operations on the frame come hereq
        alphachannel = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Create the haar cascade
        faceCascade = cv2.CascadeClassifier(r"Detection/Frontface.xml")

        # Detect faces in the image
        faces = faceCascade.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=5,minSize=(30, 30))
        #On print le nombre de visage
        print ("Found {0} faces!".format(len(faces)))

        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(alphachannel, (x, y), (x+w, y+h), (0, 0, 255), 2)
      
            ret,buffer=cv2.imencode('.jpg',alphachannel)
            frame=buffer.tobytes()

            yield(b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/index')
def index():
    return render_template('index.html')

@app.route("/livecam")
def streamcam():
    return Response(detection(),mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    