#general imports
import board
# from LEDs import *
# from audio import *
# from IO import *
from motion_detection import *
import digitalio
import busio
import time
#SD Card
import os
import adafruit_sdcard
import storage

import pio_i2s
BUFFER_SIZE = 512

properties = {  # These properties will be shared with audioeffects objects
    "buffer_size": BUFFER_SIZE, #try buffer size = 1024
    "sample_rate": 24000, # Found 24kHz works best for wav file
    "channel_count": 1,
    "bits_per_sample": 24,
    "samples_signed": True,
}

def main():
    mic = pio_i2s.I2S(
        bit_clock=board.GP14,
        word_select=board.GP15,
        data_in=board.GP13,
        **properties
        )
    
    mic.read()
            
        

# def setup_SD():
#     try:
#         cs = digitalio.DigitalInOut(board.GP8) # Chip Select
#         spi = busio.SPI(board.GP10, board.GP11, board.GP12)  # CLK, SI, SO
#         sdcard = adafruit_sdcard.SDCard(spi, cs)
#         vfs = storage.VfsFat(sdcard)
#         storage.mount(vfs, "/sd")
#     except Exception as e:
#         print("SD Card BS", e)


if __name__ == "__main__":
    main()