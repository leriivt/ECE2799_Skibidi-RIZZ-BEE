from adafruit_lsm6ds.lsm6dsox import LSM6DSOX
from adafruit_lsm6ds import Rate, AccelRange, GyroRange, AccelHPF

import board
import busio
import math
import time

class IMUController:

    def __init__(self, flight_threshold, catch_threshold, V_max):
        #we are using pins 20 and 21 for I2C
        i2c = busio.I2C(scl=board.GP21, sda=board.GP20)
        self.imu = LSM6DSOX(i2c) #.imu is an object based on the Adafruit library

        self.imu.accelerometer_range = AccelRange.RANGE_2G
        self.imu.gyro_range = GyroRange.RANGE_2000_DPS
        self.imu.accelerometer_data_rate = Rate.RATE_833_HZ
        self.imu.gyro_data_rate = Rate.RATE_833_HZ
        
        self.imu.high_pass_filter = AccelHPF.HPF_DIV100
      

        #force flight_threshold to be positive
        self.flight_threshold = abs(flight_threshold)
        
        #force catch_threshold to be positive
        self.catch_threshold = abs(catch_threshold)

        self.V_max = V_max
        
        self.flying = False
        self.velocity_x = 0
        self.velocity_y = 0
        self._last_update_time = None
        self._last_acc_x = 0
        self._last_acc_y = 0

        self.init_ax = 0
        self.init_ay = 0
        self.init_az = 0
        self.init_gx = 0
        self.init_gy = 0
        self.init_gz = 0

        self.zero_imu()

        pass
    
    def zero_imu(self, samples=50, delay=0.005):
        sum_ax = sum_ay = sum_az = 0.0
        sum_gx = sum_gy = sum_gz = 0.0
        for _ in range(samples):
            ax, ay, az = self.imu.acceleration
            gx, gy, gz = self.imu.gyro
            sum_ax += ax; sum_ay += ay; sum_az += az
            sum_gx += gx; sum_gy += gy; sum_gz += gz
            time.sleep(delay)
        self.init_ax = sum_ax / samples
        self.init_ay = sum_ay / samples
        self.init_az = sum_az / samples
        self.init_gx = sum_gx / samples
        self.init_gy = sum_gy / samples
        self.init_gz = sum_gz / samples

    
    def read_gyro(self):
        '''
        Returns a tuple with gyro data in radians/s
        '''
        
        gx, gy, gz = self.imu.gyro
        return (gx - self.init_gx, gy - self.init_gy, gz-self.init_gz)
    
    def read_acceleration(self):
        '''
        Returns a tuple with accel data in m/s^2
        '''
        ax, ay, az = self.imu.acceleration
        return (ax - self.init_ax, ay - self.init_ay, az - self.init_az)

    
    def _get_dt(self):
        '''
        Returns the fractional change in seconds between the last update and now
        '''
        now = time.monotonic()
        if self._last_update_time is None:
            self._last_update_time = now
            return 0.0
        dt = now - self._last_update_time
        self._last_update_time = now
        return dt
    
    def update_velocity(self):
        '''
        Continously integrates velocity based on the current acceleration\n
        Uses trapezoidal integration\n
        Should be run every loop while flying
        '''
        dt = min(self._get_dt(), 0.05)  # e.g. cap at 50 ms
        ax, ay, az = self.read_acceleration()

        if dt == 0 or not self.flying:
            self._last_acc_x = 0
            self._last_acc_y = 0
            return

        self.velocity_x = self.velocity_x + 0.5 * (ax + self._last_acc_x) * dt
        self.velocity_y = self.velocity_y + 0.5 * (ay + self._last_acc_y) * dt

        self._last_acc_x = ax
        self._last_acc_y = ay
        return

    def read_velocity(self):
        '''
        Returns the velocity of the frisbee
        '''
        mag = math.sqrt(self.velocity_x**2 + self.velocity_y**2)
        return mag
    
    def read_discrete_velocity(self, n):
        '''
        Returns a scaled velocity based on the max_velocity and number of discrete values to scale to

        Returns a value from 1 to n
        '''
        gx,gy,gz = self.read_gyro()
        gz = abs(gz)
        if gz > self.V_max:
            gz = self.V_max

        if self.V_max <= 0 or n <= 1:
            return 0
        
        # Scale to 1 - n
        level = int((gz / self.V_max) * (n - 1)) + 1
        #return level
        return 7

    
    def read_acceleration_mag(self):
        '''
        Returns the magnitude of the acceleration vector in a float
        '''
        ax, ay, az = self.read_acceleration()
        mag = math.sqrt(ax**2 + ay**2 + az**2)
        return mag

    def read_forward_accel(self):
        '''
        Returns the magnitude of the forward acceleration

        i.e. only the x and y axes
        '''
        ax, ay, az = self.read_acceleration()
        mag = math.sqrt(ax**2 + ay**2)
        return mag
    
    def detect_catch(self):
        '''
        Returns True if a catch is detected

        Returns False otherwise
        '''
        detect_val = False

        gx,gy,gz = self.read_gyro()

        if (gz < self.catch_threshold):
            detect_val = True
            self.flying = False

        # ax, ay, az = self.read_acceleration()
        # if (ax <= self.catch_threshold or ay <= self.catch_threshold and self.flying):
            
        #     detect_val = True

        #     self.flying = False
        
        return detect_val
    
    def detect_throw(self):
        '''
        Returns True if a throw is detected

        Returns False otherwise
        '''
        
        detect_val = False
        gx,gy,gz = self.read_gyro()
        if (gz > self.flight_threshold):
            detect_val = True
            self.flying = True

        # if (self.read_forward_accel() >= self.flight_threshold and not self.flying):
        #     detect_val = True
        #     self.flying = True
            

        
        return detect_val
    

        









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

    ("SLOPE", 0, 0, None),
    ("HPF_DIV100", 1, 0, None),
    ("HPF_DIV9", 2, 0, None),
    ("HPF_DIV400", 3, 0, None),   
'''