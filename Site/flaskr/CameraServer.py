import cv2
class CameraServer() :
    def __init__(self,sharedVariables=None, sharedFrame=None):
        self.camera= cv2.VideoCapture(0)
        self.sharedFrame = sharedFrame
        self.sharedVariables = sharedVariables

        

    def liveCam(self) :
        '''Live camera feed
        Description: this basic function will return the camera frame as a byte stream 
        Returns: the camera frame 
        '''

        while True:
            ## read the camera frame
            success,frame= self.camera.read()
            if not success:
                break
            else:
                ret,buffer=cv2.imencode('.jpg',frame)
                frame=buffer.tobytes()

            self.sharedFrame.setFrame(frame)

    