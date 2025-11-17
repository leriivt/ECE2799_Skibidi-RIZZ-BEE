import time
import board

import digitalio
import pwmio
import asyncio

from audiomp3 import MP3Decoder

try:
    from audioio import AudioOut
except ImportError:
    try:
        from audiopwmio import PWMAudioOut as AudioOut
    except ImportError:
        pass  # not always supported by every board!


# import adafruit_lsm6ds
# import audiopwmio
# import audioio


#contains state logic for the microcontroller: idle, flying, etc.
def main():

    IDLE = 0
    IN_FLIGHT = 1

    io = IOController()
    audio = AudioController()
    led = LEDController()
    imu = IMUController()

    LED_Pattern = 0

    
    while True:

        #check acceleration
        ang_acceleration = imu.read_acceleration()
        ang_orientation = imu.read_orientation()

        if(ang_acceleration <= 10):
            state = IDLE
        else:
            state = IN_FLIGHT

        #state logic
        if state == IDLE: #check buttons
            
            button = io.read_buttons()

            if button == 0: #No button pressed
                pass
            elif button == 1: #BTN1 -> Record audio
                io.record_audio()
                pass
            elif button == 2: #BTN2 -> Toggle audio
                io.toggle_audio()
                
                pass
            elif button == 3: #BTN2 -> Change LED Pattern
                led.set_pattern(LED_Pattern)
                pass
        

        elif state == IN_FLIGHT: #perform audio manipulation and output LED patterns
            
        
            audio.process_audio(ang_acceleration)
        


        time.sleep(0.01)  # 10 ms delay prevents 100% CPU usage



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
        

class AudioController:
    def __init__(self):
        #Initialize audio input/output components
        self.mic = digitalio.DigitalInOut(board.GP16) #Figure out later
        self.speaker = digitalio.DigitalInOut(board.GP2)

        wave_file = open("StreetChicken.wav", "rb")
        #wave = WaveFile(wave_file)
        #audio = AudioOut(board.A0)
        
    def process_audio(self, value):
        #Process audio input and apply effects


        pass
    def play_audio(self):
        
        
        #audio.play(wave)
        pass

    
class LEDController:
    def __init__(self):
        #Initialize LED components
        pass
    def set_pattern(self, pattern):
        
        if(pattern % 2):
            #toggle LED Modes here
            pass
        pass


class IMUController:

    # i2c = busio.I2C(board.SCL, board.SDA)
    # sox = adafruit_lsm6ds.LSM6DSOX(i2c)

    def __init__(self):
        #Initialize IMU components
        pass
    def read_orientation(self):
        #Read orientation data from IMU
        pass
    def read_acceleration(self):

        #return angular acceleration
        return 0


if __name__ == "__main__":
    main()


# #"""CircuitPython Essentials Audio Out MP3 Example"""
# import board
# import digitalio
# import time
# # import audiopwmio



# button = digitalio.DigitalInOut(board.A1)
# button.switch_to_input(pull=digitalio.Pull.UP)

# led = digitalio.DigitalInOut(board.LED)
# led.direction = digitalio.Direction.OUTPUT


# # The listed mp3files will be played in order
# mp3files = ["Claypigeons.mp3"]

# # You have to specify some mp3 file when creating the decoder
# mp3 = open(mp3files[0], "rb")
# decoder = MP3Decoder(mp3)
# audio = AudioOut(board.A0)

# while True:
#     for filename in mp3files:


#         # Updating the .file property of the existing decoder
#         # helps avoid running out of memory (MemoryError exception)
#         decoder.file = open(filename, "rb")
#         audio.play(decoder)
#         print("playing", filename)

#         # This allows you to do other things while the audio plays!
#         while audio.playing:
#             led.value = True
#             time.sleep(0.5)
#             led.value = False
#             time.sleep(0.5)

#         print("Waiting for button press to continue!")
#         while button.value:
#             pass


