import numpy as np
import cv2
import matplotlib.pyplot as plt

def Detection():
    cap = cv2.VideoCapture(0)

    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()
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
            cv2.imshow("Faces found", alphachannel)
        
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