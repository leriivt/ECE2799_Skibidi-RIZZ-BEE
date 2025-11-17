from adafruit_lsm6ds.lsm6dsox import LSM6DSOX

import board
import busio


class IMUController:

    def __init__(self):
        #we are using pins 20 and 21 for I2C
        i2c = busio.I2C(scl=board.GP21, sda=board.GP20)
        self.imu = LSM6DSOX(i2c) #.imu is an object based on the Adafruit library

        self.imu.accelerometer_range = AccelRange.RANGE_8G
        self.imu.gyro_range = GyroRange.RANGE_2000_DPS
        self.imu.accelerometer_data_rate = Rate.RATE_1_66K_HZ
        self.imu.gyro_data_rate = Rate.RATE_1_66K_HZ
        pass
    
    #returns a tuple with gyro data in radians/s
    def read_gyro(self):
        return self.imu.gryo
    
    #returns a tuple with accel data in m/s^2
    def read_acceleration(self):
        return self.imu.acceleration
    
    
    
    #check if z-axis angular velocity is greater than thresholdS
    def check_flight_z_gyro(threshold):
        return self.imu.gyro[2] > threshold




    #function to send I2C data to IMU to configure interrupt pins
    #(if we're feelin up for it)
    def configure_interrupts():
        pass








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