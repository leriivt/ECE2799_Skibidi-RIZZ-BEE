#general imports
import board
from LEDs import *
from audio import *
from IO import *
from motion_detection import *
import digitalio

#mode select
from adafruit_debouncer import Debouncer

#imu
import adafruit_lsm6ds

#audio


#SD Card
import os
import adafruit_sdcard
import storage


#leds
import neopixel


#contains state logic for the microcontroller: idle, flying, etc.

#IMPORTANT
#SD Card is only peripheral initialized within code.py, everything else within respective files
    #possible also audio so other tasks can be performed while this occurs

def main():

    IDLE = 0
    IN_FLIGHT = 1

    io = IOController()
    audio = AudioController()
    led = LEDController()
    imu = IMUController()

    LED_Pattern = 0


    #file path: "/sd"
    setup_SD()
    #PATH = '/sd/kpop.wav' #initial path to kpop demon hunters

    #For testing:
    onboard_led = digitalio.DigitalInOut(board.LED)
    onboard_led.direction = digitalio.Direction.OUTPUT


    
    while True:
        
        #check acceleration
        ang_acceleration = imu.read_acceleration() #scale from value 1-10
        ang_orientation = imu.read_orientation()   #scale from value 1-10

        if(ang_acceleration <= 5):
            state = IDLE
        else:
            state = IN_FLIGHT
            audio.process_audio(ang_acceleration) # Saves several pitch-shifted copies of the same audio file
            
            #start showin the LED pattern
            led.update_pattern()
            led.show_pattern()

        #State logic (changed to if statement since CircuitPython doesnt do match)
        if state == IDLE: 

            io.update_buttons()
                
            button = io.read_buttons()

            if button == 0: #No button pressed
                pass
                    
                    
            elif button == 1: #BTN1 -> Record audio; at this point this button has been long pressed
                        
                #turn LEDs red
                #show red LEDs
                led.record_start()
                
                audio.start_recording()

                while(io.check_recording()): #Press and hold to record audio
                    audio.record_audio()
                    io.update_buttons()

                audio.stop_recording()
                            
                #turn LEDS off
                #show leds off, reload stored pattern
                led.record_end()
                    
            elif button == 2: #BTN2 -> Toggle audio
                audio.toggle_audio()

            elif button == 3: #BTN2 -> Change LED Pattern
                led.increment_pattern()
                led.blink()
                led.update_pattern()
                    
                    
        else: #IN_FLIGHT
            #if a catch is detected:
                #led.blink(num_blinks=3, blink_time_on=0.15, blink_time_off=0.1)

            audio.play_audio(imu, led) #playaudio is blocking, needs imu and led instances to continue flight functionality
                
            
        #time.sleep(0.01)  # 10 ms delay prevents 100% CPU usage


def setup_SD():
    cs = digitalio.DigitalInOut(board.GP19) # Chip Select
    spi = busio.SPI(board.GP10, board.GP11, board.GP12)  # CLK, SI, SO
    sdcard = adafruit_sdcard.SDCard(spi, cs)
    vfs = storage.VfsFat(sdcard)
    storage.mount(vfs, "/sd")

    


if __name__ == "__main__":
    main()

