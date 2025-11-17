import time
import board


import pwmio
import asyncio


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



    


if __name__ == "__main__":
    main()

