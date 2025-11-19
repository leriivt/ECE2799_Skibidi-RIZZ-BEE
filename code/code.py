import time
import board
from LEDs import *
from IO import *

import pwmio
import asyncio


import adafruit_lsm6ds
import audiopwmio
import audioio

from audiomp3 import MP3Decoder
try:
    from audioio import AudioOut

except ImportError:
    try:
        from audiopwmio import PWMAudioOut as AudioOut
    except ImportError:
        pass  # not always supported by every board!


#contains state logic for the microcontroller: idle, flying, etc.
def main():

    IDLE = 0
    IN_FLIGHT = 1

    io = IOController()
    audio = AudioController()
    led = LEDController()
    imu = IMUController()

    LED_Pattern = 0

    #Audio stuff
    mp3files = ["Claypigeons.mp3"]
    mp3 = open(mp3files[0], "rb")
    decoder = MP3Decoder(mp3)
    audio_out = AudioOut(board.A0)

    
    while True:
        #code from 11/18 testing button for LEDs
        '''
        led.update_pattern()
    
        io.update_buttons()
    
        if io.check_LED_button():
            led.increment_pattern()
            #led.update_pattern()
            #time.sleep(0.10)
        '''
        
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
            
            while (ang_acceleration > 10): #edit condition pls

                # audio.process_audio(ang_acceleration,mp3)
                audio_temp = audio.play_audio(mp3)

                
                print("playing", mp3)

                # This allows you to do other things while the audio plays!
                while audio_temp.playing:
                    
                    audio.process_audio(ang_acceleration, mp3) #Update audio

            audio.stop()
        


        time.sleep(0.01)  # 10 ms delay prevents 100% CPU usage



    


if __name__ == "__main__":
    main()

