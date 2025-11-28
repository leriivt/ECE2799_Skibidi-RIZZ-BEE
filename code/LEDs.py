import board
import neopixel
import time

'''
    Need code for:
        - initializing LEDs
            - store which pattern
        - 
'''
NUM_PIXELS = 1

OFF = 0
RED = 1
#ORANGE = 2
#YELLOW = 3 
GREEN = 2
BLUE = 3
PURPLE = 4
#PINK = 7
RAINBOW = 5
NUM_PATTERNS = 6
NUM_STATICS = 5

DIM = 100
STATIC_RAINBOW = 101

colors = {
    OFF : [(0 ,0, 0)] * NUM_PIXELS,
    RED : [(255, 0, 0)] * NUM_PIXELS,
    #ORANGE : (255, 128, 0),
    #YELLOW : (255, 255, 51),
    GREEN : [(51, 255, 51)] * NUM_PIXELS,
    BLUE : [(0, 128, 255)] * NUM_PIXELS,
    PURPLE : [(153, 51, 255)] * NUM_PIXELS,
    #PINK : (255, 51, 153),
    RAINBOW : [(255, 255, 51)] * NUM_PIXELS,
    DIM : [(20 ,20, 20)] * NUM_PIXELS
}

class LEDController:
    
    def __init__(self, pattern=RED, static=1, brightness=0.5):
        self.pattern = pattern
        self.static = static
        self.num_pixels = NUM_PIXELS
        
        self.pixels = neopixel.NeoPixel(board.GP22, self.num_pixels)
        self.pixels.brightness = brightness
        self.pixels.auto_write = False
        #Initialize LED components
        pass
        
    def increment_pattern(self):        
        self.pattern += 1
         
        if self.pattern >= NUM_PATTERNS:
            self.pattern = 0
            self.static = 1
        elif self.static and self.pattern >= NUM_STATICS:
            self.static = 0
        pass
    
    '''
    if a dynamic pattern, updates pattern
    '''
    def update_pattern(self, pattern=None):
        if pattern == None:
            pattern = self.pattern
        self.pixels[:] = colors[pattern]
    
    def show_pattern(self):
        self.pixels.show()
    
    def blink(self, pattern=None, num_blinks=1, blink_time_on=0.5, blink_time_off=0):
        if self.pattern == OFF:
            pattern = DIM
            
        self.update_pattern(pattern=OFF)
        self.show_pattern()
        time.sleep(0.1)
        
        for x in range(num_blinks):
            
            
            self.update_pattern(pattern)
            self.show_pattern()
            time.sleep(blink_time_on)
            
            self.update_pattern(pattern=OFF)
            self.show_pattern()
            time.sleep(blink_time_off)
        pass
    
    def record_start(self):
        self.update_pattern(RED)
        self.show_pattern()
        pass
    
    def record_end(self):
        self.update_pattern(OFF)
        self.show_pattern()
        self.update_pattern(OFF)
        pass




