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

def main():
    imu = IMUController(0, 10)
    setup_SD()
    iterations = 0

    with open("/sd/imu_data.txt", "w", encoding="utf-8") as f:
        print("File opened sucessfully")
        f.write("SD Card Data:\n")
        while iterations < 10:
            f.write("Sample:")
            f.write(str(imu.read_acceleration()))
            f.write(str(imu.read_gyro()))
            f.write("\n")
            iterations += 1
            time.sleep(1)
        f.close()

            
        

def setup_SD():
    try:
        cs = digitalio.DigitalInOut(board.GP8) # Chip Select
        spi = busio.SPI(board.GP10, board.GP11, board.GP12)  # CLK, SI, SO
        sdcard = adafruit_sdcard.SDCard(spi, cs)
        vfs = storage.VfsFat(sdcard)
        storage.mount(vfs, "/sd")
    except Exception as e:
        print("SD Card BS", e)


if __name__ == "__main__":
    main()