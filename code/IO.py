import digitalio
import board

class IOController:
    
    def __init__(self):
        #Initialize buttons, switches, leds, amplifier, microphone
        self.BTN_LED = digitalio.DigitalInOut(board.GP10)
        self.BTN_LED.direction = digitalio.Direction.INPUT
        self.BTN_LED.pull = digitalio.Pull.UP
        self.BTN_record = digitalio.DigitalInOut(board.GP11)
        self.BTN_record.direction = digitalio.Direction.INPUT
        self.BTN_record.pull = digitalio.Pull.UP
        self.BTN_audio_sel = digitalio.DigitalInOut(board.GP12)
        self.BTN3_audio_sel.direction = digitalio.Direction.INPUT
        self.BTN3_audio_sel.pull = digitalio.Pull.UP
        

    def read_buttons(self): #active low buttons
    
        if(not self.BTN_LED.value):
            return 1
        elif(not self.BTN_record.value):
            return 2
        elif(not self.BTN_audio_sel.value):
            return 3
        else: #No button pressed
            return 0
        
    def toggle_audio(self): #toggle between microphone recorded audio & Kpop demon hunters

        pass

    def record_audio(self):

        pass