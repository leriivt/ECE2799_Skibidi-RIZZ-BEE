import board
import neopixel
import time
from rainbowio import colorwheel

'''
    Need code for:
        - initializing LEDs
            - store which pattern
        - 
'''
NUM_PIXELS = 12

OFF = 0
RED = 1
#ORANGE = 2
#YELLOW = 3 
GREEN = 2
BLUE = 3
PURPLE = 4
#PINK = 7
RAINBOW = 5
HUNTRIX = 6
GOLDEN = 7
NUM_PATTERNS = 8
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
    RAINBOW : [(255, 255, 255)] * NUM_PIXELS, #placeholder
    HUNTRIX : [(255, 255, 255)] * NUM_PIXELS, #placeholder
    GOLDEN : [(255, 255, 255)] * NUM_PIXELS,  #placeholder
    DIM : [(20 ,20, 20)] * NUM_PIXELS
}

animation_delay = {
    RAINBOW : 0.02,
    HUNTRIX : 0.02,
    GOLDEN : 0.13
}

def hue_cycle(current, start, end, multiplier, num_pixels):
    hue_length = (end-start)*2
    current = current % hue_length
    pixel_list = [0] * num_pixels
    for pixel in range(num_pixels):
        pixel_index = (pixel * (hue_length+1) // num_pixels) + current * multiplier
        pixel_index = pixel_index % hue_length
        pixel_index += start
        if pixel_index > end:
            pixel_index = 2*end - pixel_index
        pixel_list[pixel] = colorwheel(pixel_index)
    return pixel_list

def rainbow_cycle(current, num_pixels):
    color = current % 255
    pixel_list = [0] * num_pixels
    for pixel in range(num_pixels):
        pixel_index = (pixel * 256 // num_pixels) + color * 5
        pixel_list[pixel] = colorwheel(pixel_index & 255)
    return pixel_list

colors[RAINBOW] = rainbow_cycle(0, NUM_PIXELS)
colors[HUNTRIX] = hue_cycle(0, 110, 230, 5, NUM_PIXELS)
colors[GOLDEN] = hue_cycle(0, 14, 22, 4, NUM_PIXELS)

class LEDController:
    
    def __init__(self, pattern=RED, static=1, brightness=0.5):
        self.pattern = pattern
        self.static = static
        self.dynamic_offset = 0 #offset for cycling through dynamic patterns
        self.last_update = 0
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
        self.last_update = time.monotonic()
        
    def dynamic_update_show(self):
        current_time = time.monotonic()
        if (not self.static) and (current_time - self.last_update >= animation_delay[self.pattern]):
            if self.pattern == RAINBOW:
                pixel_list = rainbow_cycle(self.dynamic_offset, self.num_pixels)
            elif self.pattern == HUNTRIX:
                pixel_list = hue_cycle(self.dynamic_offset, 110, 230, 5, self.num_pixels)
            else: #GOLDEN
                pixel_list = hue_cycle(self.dynamic_offset, 14, 22, 4, self.num_pixels)
            
            self.last_update = current_time
            self.dynamic_offset += 1
            self.pixels[:] = pixel_list
            self.show_pattern()
    
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
    
    
    #-----------------------------------------------
    def rainbow_cycle(self, wait):
        for color in range(255):
            for pixel in range(len(self.pixels)):
                pixel_index = (pixel * 256 // len(self.pixels)) + color * 5
                self.pixels[pixel] = colorwheel(pixel_index & 255)
            self.pixels.show()
            time.sleep(wait)
            
    def galaxy_cycle(self, wait): #colorwheel vales 110 to 230
        for color in range(240):
            for pixel in range(len(self.pixels)):
                pixel_index = (pixel * 241 // len(self.pixels)) + color * 5
                pixel_index = pixel_index % 240
                pixel_index += 110
                if pixel_index > 230:
                    pixel_index = 2*230 - pixel_index
                self.pixels[pixel] = colorwheel(pixel_index)
            self.pixels.show()
            time.sleep(wait)
            
    def hue_cycle_testing(self, start, end, multiplier, wait):
        length = (end-start)*2
        for color in range(length):
            for pixel in range(len(self.pixels)):
                pixel_index = (pixel * (length+1) // len(self.pixels)) + color * multiplier
                pixel_index = pixel_index % length
                pixel_index += start
                if pixel_index > end:
                    pixel_index = 2*end - pixel_index
                self.pixels[pixel] = colorwheel(pixel_index)
            self.pixels.show()
            time.sleep(wait)
    '''        
    def hue_cycle(self, current, start, end, multiplier, wait):
        length = (end-start)*2
        current = current % length
            for pixel in range(len(self.pixels)):
                pixel_index = (pixel * (length+1) // len(self.pixels)) + color * multiplier
                pixel_index = pixel_index % length
                pixel_index += start
                if pixel_index > end:
                    pixel_index = 2*end - pixel_index
                self.pixels[pixel] = colorwheel(pixel_index)
            self.pixels.show()
            time.sleep(wait)
    '''




