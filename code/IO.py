import digitalio
import board

class IOController:
    
    def __init__(self):
        #Initialize buttons, switches, leds, amplifier, microphone
        self.BTN1 = digitalio.DigitalInOut(board.D2)
        self.BTN1.direction = digitalio.Direction.INPUT
        self.BTN1.pull = digitalio.Pull.UP
        self.BTN2 = digitalio.DigitalInOut(board.D3)
        self.BTN2.direction = digitalio.Direction.INPUT
        self.BTN2.pull = digitalio.Pull.UP
        self.BTN3 = digitalio.DigitalInOut(board.D4)
        self.BTN3.direction = digitalio.Direction.INPUT
        self.BTN3.pull = digitalio.Pull.UP
        

    def read_buttons(self): #active low buttons
    
        if(not self.BTN1.value):
            return 1
        elif(not self.BTN2.value):
            return 2
        elif(not self.BTN3.value):
            return 3
        else: #No button pressed
            return 0
        
    def toggle_audio(self): #toggle between microphone recorded audio & Kpop demon hunters

        pass

    def record_audio(self):

        pass