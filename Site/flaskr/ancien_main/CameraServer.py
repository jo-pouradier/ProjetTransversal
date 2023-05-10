import cv2
import os


class CameraServer:
    def __init__(self, sharedVariables=None, sharedFrame=None):
        self.cap = cv2.VideoCapture(0)
        self.sharedFrame = sharedFrame
        self.sharedVariables = sharedVariables
        self.front_face_path = os.path.join(os.path.dirname(__file__), 'haarcascade_frontalface_default.xml')
        self.cam_config = {
            "compteur" : 0,
            "anglex" : 0,
            "angley" : 0,
            "FPS" : 60,
            "WIDTH" : 5,
            "HEIGHT" : 5,
            "faceCascade" : cv2.CascadeClassifier(self.front_face_path)
        }

        self.cam_config["Screenmiddle"] = (self.cam_config["WIDTH"] // 2, self.cam_config["HEIGHT"] // 2)
        self.cam_config["RapportConvx"] = (2 / self.cam_config["WIDTH"])
        self.cam_config["RapportConvy"] = (2 / self.cam_config["HEIGHT"])

        # Implementing our parameters
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.cam_config["WIDTH"])
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.cam_config["HEIGHT"])
        self.cap.set(cv2.CAP_PROP_FPS, self.cam_config["FPS"])

    def liveCam(self):
        '''Live camera feed
        Description: this basic function will return the camera frame as a byte stream 
        Returns: the camera frame 
        '''
        print("livecam")

        while True:
            # read the camera frame
            success, frame = self.cap.read()

            if not success:
                break
            else:
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()

            self.sharedFrame.setFrame(frame)

    def Detection(self):
        while True:
            # Local variables
            airemax = 0
            Centreproche = 0

            # Capture frame-by-frame
            ret, frame = self.cap.read()
            # Our operations on the frame come here
            # alphachannel = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Create the haar cascade

            # Detect faces in the image
            faces = self.cam_config["faceCascade"].detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30)
            )
            
            
            # Draw a rectangle around the faces
            for (x, y, w, h) in faces:
                
                #cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 255, 255), 2)
                #Calcul the area of the rectangle
                airelocale=int(abs(x+w-x)*abs(y+h-y))
                #Only keeping in memory the largest recangle
                
                
                if airelocale>=airemax:
                    airemax=airelocale
                    #Converting the pixel-distance  pixel in angular distance for the servo motor
                    Centreproche=((x+x+w)/2,(y+h+y)/2)

                if airelocale >= airemax:
                    airemax = airelocale
                    # Converting the pixel-distance  pixel in angular distance for the servo motor
                    Centreproche = ((x + x + w) / 2, (y + h + y) / 2)

                    self.cam_config["anglex"] = (Centreproche[0] - self.cam_config["Screenmiddle"][0]) * \
                                                self.cam_config["RapportConvx"] + 1.5
                    self.cam_config["angley"] = (Centreproche[1] - self.cam_config["Screenmiddle"][1]) * \
                                                self.cam_config["RapportConvy"] + 1.5

            # Printing the number of face found
            print("Found {0} faces!".format(len(faces)))

            self.cam_config["compteur"] += 1
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            self.sharedFrame.setFrame(frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    def run(self):
        self.liveCam()
