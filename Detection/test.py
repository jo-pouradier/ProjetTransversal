import numpy as np
import cv2
import time


faceCascade = cv2.CascadeClassifier('Frontface.xml')
print(cv2.CAP_DSHOW)
cap = cv2.VideoCapture(0)
cap.set(3,640) # set Width
cap.set(4,480) # set Height
# cap.set(cv2.CAP_PROP_FPS, 20)
cv2.setUseOptimized(True)
cv2.setNumThreads(1)

FPS = 120
timer = 1/FPS
count_fps = 0
timer_fps = time.perf_counter()
prev_frame_time = 0
new_frame_time = 1

img = None

count = 0
while True:
    
    ret, img = cap.read()
    # filp image horizontaly like mirror
    img = cv2.flip(img, 1)
    # waiting fps
    # if new_frame_time - prev_frame_time < timer:
    #     time.sleep(timer - (new_frame_time - prev_frame_time))

    count+=1
    print(count)

    fps = cap.get(cv2.CAP_PROP_FPS)
    print("Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}".format(fps))
    # get fps
    count_fps += 1
    if time.perf_counter() - timer_fps > 1:
        timer_fps = time.perf_counter()
        print("FPS: ", count_fps)
        count_fps = 0
    
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
    fps = 1/(new_frame_time-prev_frame_time)
    prev_frame_time = new_frame_time
    new_frame_time = time.perf_counter()
    cv2.putText(img, text=str(np.round(fps, 1)), org=(7, 70), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(0, 0, 0), thickness=2, lineType=cv2.LINE_AA)

    cv2.imshow('video',img)
    #interupt
    k = cv2.waitKey(30) & 0xFF
    if k == ord('q'): # press 'q' to quit
        break

cap.release()
cv2.destroyAllWindows()