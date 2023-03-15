from flask import Flask,Response,render_template
import cv2,time
import numpy as np


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

def detectionV2() :
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


@app.route('/index')
def index():
    return render_template('index.html')

@app.route("/livecam")
def streamcam():
    return Response(detectionV2(),mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
    