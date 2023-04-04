import numpy as np
import cv2
import matplotlib.pyplot as plt

def Detection():

    
    compteur=0
    Anglex=0
    Angley=0


    #Camera variables
    FPS=10
    WIDTH=320
    HEIGHT=240
    Screenmiddle=(WIDTH//2,HEIGHT//2)
    #Conversion in degrees
    RapportConv=90/WIDTH


    cap = cv2.VideoCapture(0)
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
            #On calcule l'aire du rectangle 
            airelocale=int(abs(x+w-x)*abs(y+h-y))
            #On garde en mémoire uniquement le plus grand rectangle
            if airelocale>=airemax:
                airemax=airelocale
                #On convertit la distance en pixel en distance "angulaire" pour le servomoteur
                Centreproche=(  (x+x+w)/2,(y+h+y)/2)
                Anglex=int((Centreproche[0]-Screenmiddle[0])*RapportConv)
                Angley=int((Centreproche[1]-Screenmiddle[1])*RapportConv)
            cv2.imshow("Faces found", frame)
        


        #On print l'angle de rotation du servo afin de centrer la camera sur l'image
        print(Anglex,Angley)
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