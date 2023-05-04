import serial as ser

class RobotServer() :
    def __init__(self,sharedVariables=None, sharedFrame=None) :
        self.commandes = {
        'z' : 'avancerR\r',
        'q' : 'gaucheR\r',
        's' : 'arriereR\r',
        'd' : 'droiteR\r',
        ' ' : 'stop\r',
        'ArrowUp' : 'hautC\r',
        'ArrowDown' : 'basC\r',
        'ArrowLeft' : 'gaucheC\r',
        'ArrowRight' : 'droiteC\r',
        'Enter' : 'stop\r',
        }
        self.sharedVariables = sharedVariables
    def send_commands(self):
        if self.sharedVariables['commande']['key'] in self.commandes.keys():
            ser.write(bytes(self.commandes[self.sharedVariables['commande']['key']], 'utf8'))
            return 200
        else : 
            print("stop")
            ser.write(bytes("stop\r", 'utf8'))
            return 400


    def run(self) :
        while True :
            self.send_commands()
