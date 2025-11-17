from adafruit_lsm6ds.lsm6dsox import LSM6DSOX

import board
import busio

#initialize the IMU, set its input pins
i2c = busio.I2C(scl=board.GP21, sda=board.GP20)
sox = LSM6DSOX(i2c)

sensor.accelerometer_range = AccelRange.RANGE_8G
sensor.gyro_range = GyroRange.RANGE_2000_DPS
sensor.accelerometer_data_rate = Rate.RATE_1_66K_HZ
sensor.gyro_data_rate = Rate.RATE_1_66K_HZ

#check if z-axis angular velocity is greater than thresholdS
def check_flight(threshold):
    return sox.gyro[2] > threshold

#function to send I2C data to IMU to configure interrupt pins
def configure_interrupts():



#possible data rates and ranges    
 '''   
    ("RATE_SHUTDOWN", 0, 0, None),
    ("RATE_12_5_HZ", 1, 12.5, None),
    ("RATE_26_HZ", 2, 26.0, None),
    ("RATE_52_HZ", 3, 52.0, None),
    ("RATE_104_HZ", 4, 104.0, None),
    ("RATE_208_HZ", 5, 208.0, None),
    ("RATE_416_HZ", 6, 416.0, None),
    ("RATE_833_HZ", 7, 833.0, None),
    ("RATE_1_66K_HZ", 8, 1666.0, None),
    ("RATE_3_33K_HZ", 9, 3332.0, None),
    ("RATE_6_66K_HZ", 10, 6664.0, None),
    ("RATE_1_6_HZ", 11, 1.6, None),   

    ("RANGE_125_DPS", 125, 125, 4.375),
    ("RANGE_250_DPS", 0, 250, 8.75),
    ("RANGE_500_DPS", 1, 500, 17.50),
    ("RANGE_1000_DPS", 2, 1000, 35.0),
    ("RANGE_2000_DPS", 3, 2000, 70.0),   

    ("RANGE_2G", 0, 2, 0.061),
    ("RANGE_16G", 1, 16, 0.488),
    ("RANGE_4G", 2, 4, 0.122),
    ("RANGE_8G", 3, 8, 0.244),    
'''