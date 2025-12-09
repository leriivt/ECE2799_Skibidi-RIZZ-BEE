import board
import digitalio
import time
from LEDs import *
from motion_detection import *

#audio out
import audiocore
from audiopwmio import PWMAudioOut as AudioOut
import adafruit_wave 
from audiocore import WaveFile

import adafruit_sdcard
import storage

#microphone
import pio_i2s

#pitch shifting
from audiobusio import I2SOut
from audiocore import RawSample
from audiodelays import PitchShift

from audio import *
from LEDs import *

def setup_SD():
    try:
        cs = digitalio.DigitalInOut(board.GP8) # Chip Select
        spi = busio.SPI(board.GP10, board.GP11, board.GP12)  # CLK, SI, SO
        sdcard = adafruit_sdcard.SDCard(spi, cs)
        vfs = storage.VfsFat(sdcard)
        storage.mount(vfs, "/sd")
    except Exception as e:
        print("SD Card BS:", e)

setup_SD()

path = "/sd/kpop.wav"

a = AudioController()
led = LEDController()

try:
    f = open(path, "rb")

    wave = WaveFile(f)
    # print("sample_rate:", wave.sample_rate, "channels:", wave.channel_count)
    print("Playing...")
    
    a.pitchshift.semitones = 0

    onboard_led = digitalio.DigitalInOut(board.LED)
    onboard_led.direction = digitalio.Direction.OUTPUT
    
    
    while True:

        a.pitchshift.play(wave)
        a.audio.play(a.pitchshift)

        while a.audio.playing:
            onboard_led = True
            time.sleep(0.5)
            onboard_led = False
            time.sleep(0.5)

            

        
        
    # f.close()

except Exception as e:
    print("Audio error:", e)
    time.sleep(2)
    





