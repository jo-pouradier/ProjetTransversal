#include <opencv2/opencv.hpp>

using namespace cv;

int main() {
    // Initialiser le flux vidéo de la webcam
    cv::VideoCapture::VideoCapture cap(0);
    
    // Initialiser le détecteur de visages
    CascadeClassifier face_cascade;
    face_cascade.load("haarcascade_frontalface_default.xml");
    
    while (true) {
        // Lire la frame courante de la webcam
        Mat frame;
        cap >> frame;
        
        // Convertir l'image en noir et blanc pour accélérer la détection
        Mat gray;
        cvtColor(frame, gray, cv::COLOR_BGR2GRAY);
        
        // Détecter les visages dans l'image
        std::vector<Rect> faces;
        face_cascade.detectMultiScale(gray, faces, 1.3, 5);
        
        // Dessiner un rectangle autour de chaque visage détecté
        for (size_t i = 0; i < faces.size(); i++) {
            rectangle(frame, faces[i], Scalar(255, 0, 0), 2);
        }
        
        // Afficher la frame avec les visages détectés
        imshow("frame", frame);
        
        // Attendre que l'utilisateur appuie sur la touche 'q' pour quitter
        if (waitKey(1) == 'q') {
            break;
        }
    }
    
    // Relâcher la webcam
    cap.release();
    destroyAllWindows();
    
    return 0;
}

// on peut reduire la taille de l'image pour accélérer la détection:
// cap.set(CAP_PROP_FRAME_WIDTH, 320); // largeur = 320
// cap.set(CAP_PROP_FRAME_HEIGHT, 240); // hauteur = 240
