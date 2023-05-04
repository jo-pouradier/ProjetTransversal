#import Cam
#import Commandes
from threadutils import ThreadSafeFrame, ThreadSafeDict
import cv2
import multiprocessing
from flaskserver import FlaskServer
#from cameraserver import CameraServer
#from robotserver import RobotServer




class App :
    def __init__(self) :
        self.sharedVariables = ThreadSafeDict()
        
        
        cap = cv2.VideoCapture(0) # Replace 0 with your camera index if you have multiple cameras
        res, image = cap.read()
        cap.release()
        # Définir les paramètres pour l'encodage JPEG
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY),50]
        ret,buffer = cv2.imencode('.jpg', image, encode_param)
        # On définie un objet multiprocess safe pour stocker l'image
        self.sharedFrame = ThreadSafeFrame(len(buffer.tobytes())*5)

    def run(self):
        print("Starting threads")
        self.cameraProcess = multiprocessing.Process(target=runCameraServer, args=(self.sharedVariables, self.sharedFrame))
        self.cameraProcess.start()
        self.flaskProcess = multiprocessing.Process(target=runFlaskServer, args=(self.sharedVariables, self.sharedFrame))
        self.flaskProcess.start()
        #self.robotProcess = multiprocessing.Process(target=runRobotServer, args=(self.sharedVariables, self.sharedFrame))
        #self.robotProcess.start()
        #if (input("Press enter to stop\n") == 'n'):
            #self.cameraProcess.terminate()
            #self.flaskProcess.terminate()
            #self.robotProcess.terminate()
            #print("Threads stopped")

    
def runFlaskServer(sharedVariables, sharedFrame):
    flaskServer = FlaskServer(sharedVariables, sharedFrame)
    flaskServer.run()
    
def runCameraServer(sharedVariables, sharedFrame):
    cameraServer = CameraServer(sharedVariables, sharedFrame)
    cameraServer.run()

def runRobotServer(config, sharedVariables, sharedFrame):
    robotServer = RobotServer(config, sharedVariables, sharedFrame)
    robotServer.run()

if __name__ == '__main__':
    app = App()
    app.run()