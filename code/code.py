#general imports
import board
from LEDs import *
from audio import *
from IO import *
from motion_detection import *
import digitalio

#SD Card
import os
import adafruit_sdcard
import storage

#contains state logic for the microcontroller: idle, flying, etc.

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
        gyro = imu.read_gyro()   #scale from value 1-10

        if(ang_acceleration <= 5):
            state = IDLE
        else:
            state = IN_FLIGHT
            
            #start showin the LED pattern
            led.update_pattern()
            led.show_pattern()

        #State logic (changed to if statement since CircuitPython doesnt do match)
        if state == IDLE: 

            audio.speaker_off()

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
                
            audio.speaker_on()
            audio.play_audio(imu, led) #playaudio is blocking, needs imu and led instances to continue flight functionality

            state = IDLE
                
            
        #time.sleep(0.01)  # 10 ms delay prevents 100% CPU usage


def setup_SD():
    try:
        cs = digitalio.DigitalInOut(board.GP8) # Chip Select
        spi = busio.SPI(board.GP10, board.GP11, board.GP12)  # CLK, SI, SO
        sdcard = adafruit_sdcard.SDCard(spi, cs)
        vfs = storage.VfsFat(sdcard)
        storage.mount(vfs, "/sd")
    except Exception as e:
        print("SD Card BS:", e)

    


if __name__ == "__main__":
    main()

