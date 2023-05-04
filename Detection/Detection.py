import numpy as np
import cv2
import matplotlib.pyplot as plt

def Detection():

    
    compteur=0
    Anglex=0
    Angley=0


    #Camera variables
    FPS=8
    WIDTH=320
    HEIGHT=240

    #Finding the middle of the screen
    Screenmiddle=(WIDTH//2,HEIGHT//2)
    #Conversion in degrees
    RapportConvx= (2/WIDTH)
    RapportConvy= (2/HEIGHT)


    cap = cv2.VideoCapture(0)


    #Implementing our parameters
    ret = cap.set(cv2.CAP_PROP_FRAME_WIDTH,WIDTH) 
    ret = cap.set(cv2.CAP_PROP_FRAME_HEIGHT,HEIGHT)
    ret = cap.set(cv2.CAP_PROP_FPS,FPS)






    while(True):
        

    
        #Local variables
        airemax=0
        Centreproche=0


        # Capture frame-by-frame
        ret, frame = cap.read()
        # Our operations on the frame come hereq
        #alphachannel = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)       
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Create the haar cascade
        faceCascade = cv2.CascadeClassifier(r"Detection/Frontface.xml")
        # Detect faces in the image
        faces = faceCascade.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=5,minSize=(30, 30))

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
                Centreproche=(  (x+x+w)/2,(y+h+y)/2)
                Anglex=(Centreproche[0]-Screenmiddle[0])*RapportConvx + 1.5
                Angley=(Centreproche[1]-Screenmiddle[1])*RapportConvy  + 1.5
            # cv2.imshow("Faces found", frame)
        


        #Printing the angle of rotation (to centralize the camera on the face) 
        print(Anglex,Angley)
        #Printing the number of face
        print ("Found {0} faces!".format(len(faces)))

        compteur+=1


        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

            
    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
    return()
 
Detection()
