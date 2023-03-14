import cv2

# Initialiser le flux vidéo de la webcam
cap = cv2.VideoCapture(0)
cap.set(3, 320) # largeur = 320
cap.set(4, 240) # hauteur = 240
# Initialiser le détecteur de visages
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

while True:
    # Lire la frame courante de la webcam
    ret, frame = cap.read()
    
    # Convertir l'image en noir et blanc pour accélérer la détection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Détecter les visages dans l'image
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
    
    # Dessiner un rectangle autour de chaque visage détecté
    for (x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
    
    # Afficher la frame avec les visages détectés
    cv2.imshow('frame',frame)
    
    # Attendre que l'utilisateur appuie sur la touche 'q' pour quitter
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Fermer la fenêtre d'affichage et relâcher la webcam
cap.release()
cv2.destroyAllWindows()


# on peut reduire la taille de la video pour accélérer la détection:
# cap.set(3, 320) # largeur = 320
# cap.set(4, 240) # hauteur = 240
