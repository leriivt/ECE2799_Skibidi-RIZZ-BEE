import digitalio
import board
from adafruit_debouncer import Debouncer
from adafruit_debouncer import Button

class IOController:


    
    def __init__(self):
        #Initialize buttons 
        self.BTN_record_pin = digitalio.DigitalInOut(board.GP0)
        self.BTN_record_pin.direction = digitalio.Direction.INPUT
        self.BTN_record_pin.pull = digitalio.Pull.UP
        self.BTN_record = Button(self.BTN_record_pin)
        
        self.BTN_audio_sel_pin = digitalio.DigitalInOut(board.GP1)
        self.BTN_audio_sel_pin.direction = digitalio.Direction.INPUT
        self.BTN_audio_sel_pin.pull = digitalio.Pull.UP
        self.BTN_audio_sel = Button(self.BTN_audio_sel_pin)
        
        self.BTN_LED_pin = digitalio.DigitalInOut(board.GP5)
        self.BTN_LED_pin.direction = digitalio.Direction.INPUT
        self.BTN_LED_pin.pull = digitalio.Pull.UP
        self.BTN_LED = Button(self.BTN_LED_pin)

        
    def update_buttons(self):
        self.BTN_record.update()
        self.BTN_audio_sel.update()
        self.BTN_LED.update()
        pass
    
    '''    
    def check_LED_button(self):
        #1 if not pressed
        #we want 1 if pressed, so add a not
        return self.BTN_LED.pressed
    '''
    
    def read_buttons(self): #active low buttons
    
        if(self.BTN_record.pressed):
            return 1
        elif(self.BTN_audio_sel.pressed):
            return 2
        elif(self.BTN_LED.pressed):
            return 3
        else: #No button pressed
            return 0
        
    def check_recording(self):
        return not self.BTN_record.released