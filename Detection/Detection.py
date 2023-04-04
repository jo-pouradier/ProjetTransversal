import numpy as np
import cv2
import matplotlib.pyplot as plt

def Detection():

    #Local variables
    
    normmax=0
    Centreproche=0
    compteur=0
    RapportConv=9/32

    
    FPS=10
    WIDTH=320
    HEIGHT=240
    Screenmiddle=(WIDTH/2,HEIGHT/2)


    cap = cv2.VideoCapture(0)
    ret = cap.set(cv2.CAP_PROP_FRAME_WIDTH,WIDTH) 
    ret = cap.set(cv2.CAP_PROP_FRAME_HEIGHT,HEIGHT)
    ret = cap.set(cv2.CAP_PROP_FPS,FPS)






    while(True):
        
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
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
            if compteur%(FPS//2) == 0:
                normlocal=np.sqrt( abs(x+w-x)**2 + abs(y+h-y) **2  )
                if normlocal>=normmax:
                    Centreproche=(  (x+x+w)/2,(y+h+y)/2)
                    Anglex=int((Centreproche[0]-Screenmiddle[0])*RapportConv)
                    Angley=int((Centreproche[1]-Screenmiddle[1])*RapportConv)
                    print(Anglex,Angley)
            cv2.imshow("Faces found", frame)
        
        #On print le nombre de visage
        print ("Found {0} faces!".format(len(faces)))
        compteur+=1
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

            
    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
    return()
 
 



Detection()




#def liveCam() :
  #  cap = cv2.VideoCapture(0)
   # while(True):
        # Capture frame-by-frame
    #    ret, frame = cap.read()
        # Our operations on the frame come hereq
     #   cv2.imshow("Faces found", frame)
      #  if cv2.waitKey(1) & 0xFF == ord('q'):
       #     break

    # When everything done, release the capture
    #cap.release()
    #cv2.destroyAllWindows()
    #return()

#liveCam()