import cv2
import numpy as np

class CameraServer() :
    def __init__(self,sharedVariables=None, sharedFrame=None):
        self.cap= cv2.VideoCapture(0)
        self.sharedFrame = sharedFrame
        self.sharedVariables = sharedVariables
        self.cam_config = {
            "compteur" : 0,
            "anglex" : 0,
            "angley" : 0,
            "FPS" : 8,
            "WIDTH" : 320,
            "HEIGHT" : 240,
            "faceCascade" : cv2.CascadeClassifier(r'Site\flaskr\haarcascade_frontalface_default.xml')
        }

        self.cam_config["Screenmiddle"] = (self.cam_config["WIDTH"]//2,self.cam_config["HEIGHT"]//2)
        self.cam_config["RapportConvx"] = (2/self.cam_config["WIDTH"])
        self.cam_config["RapportConvy"] = (2/self.cam_config["HEIGHT"])
        

    def liveCam(self) :
        '''Live camera feed
        Description: this basic function will return the camera frame as a byte stream 
        Returns: the camera frame 
        '''
        print("livecam")

        while True:
            ## read the camera frame
            success,frame= self.cap.read()
            if not success:
                break
            else:
                ret,buffer=cv2.imencode('.jpg',frame)
                frame=buffer.tobytes()

            self.sharedFrame.setFrame(frame)

    def Detection(self):

        #Implementing our parameters
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH,self.cam_config["WIDTH"]) 
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT,self.cam_config["HEIGHT"])
        self.cap.set(cv2.CAP_PROP_FPS,self.cam_config["FPS"])

        while True:
            #Local variables
            airemax=0
            Centreproche=0


            # Capture frame-by-frame
            ret, frame = self.cap.read()
            # Our operations on the frame come hereq
            #alphachannel = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)       
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Create the haar cascade
            
            # Detect faces in the image
            faces = self.cam_config["faceCascade"].detectMultiScale(gray,scaleFactor=1.1,minNeighbors=5,minSize=(30, 30))

            # Draw a rectangle around the faces
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 255, 255), 2)
                #Calcul the area of the rectangle
                airelocale=int(abs(x+w-x)*abs(y+h-y))
                face_color = frame[y:y + h, x:x + w]
                #Only keeping in memory the largest recangle
                
                
                if airelocale>=airemax:
                    airemax=airelocale
                    #Converting the pixel-distance  pixel in angular distance for the servo motor
                    
                    Anglex=(Centreproche[0]-self.cam_config["Screenmiddle[0]"])*self.cam_config["RapportConvx"] + 1.5
                    Angley=(Centreproche[1]-self.cam_config["Screenmiddle[1]"])*self.cam_config["RapportConvy"]  + 1.5
                # cv2.imshow("Faces found", frame)
            


            #Printing the angle of rotation (to centralize the camera on the face) 
            print(Anglex,Angley)
            #Printing the number of face found
            print ("Found {0} faces!".format(len(faces)))

            self.cam_config["compteur"]+=1
            self.sharedFrame.setFrame(frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

                
        # When everything done, release the capture
        self.cap.release()
    def run(self) :
        self.Detection()