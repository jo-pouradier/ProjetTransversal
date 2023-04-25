import cv2
face_cascade=cv2.CascadeClassifier(r"Detection/Frontface.xml")
smile_cascade = cv2.CascadeClassifier(r"Detection/Smile.xml")
cap = cv2.VideoCapture(0)
while cap.isOpened():
    _, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    smiles = smile_cascade.detectMultiScale(gray, 2, 4)
    faces = face_cascade.detectMultiScale(gray, 2, 4)
    for (x1, y1, w1, h1) in faces:
        cv2.rectangle(img, (x1, y1), (x1 + w1, y1 + h1), (255, 0, 0), 3)
        face_gray= gray[y1:y1 + h1, x1:x1 + w1]
        face_color = img[y1:y1 + h1, x1:x1 + w1]
        for (x, y , w ,h) in smiles:
            cv2.rectangle(face_color, (x,y), (x+w, y+h), (0, 0 ,255), 3)
    
    cv2.imshow('img', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()