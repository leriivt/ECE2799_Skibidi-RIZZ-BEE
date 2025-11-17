import board
import neopixel

'''
    Need code for:
        - initializing LEDs
            - store which pattern
        - 
'''
OFF = 0
RED = 1
ORANGE = 2
YELLOW = 3 
GREEN = 4
BLUE = 5
PURPLE = 6
PINK = 7
RAINBOW = 8
NUM_PATTERNS = 9
NUM_STATICS = 8

class LEDController:
    
    def __init__(self, pattern=RED, static=1):
        self.pattern = pattern
        self.static = static
        self.num_pixels = 12
        
        self.pixels = neopixel.NeoPixel(board.GP22, num_pixels)
        self.pixels.brightness = 0.5
        #Initialize LED components
        pass
        
    def increment_pattern(self):        
        self.pattern += 1
        if self.pattern >= NUM_PATTERNS:
            self.patern = 0
            self.static = 1
        else if self.static && self.pattern >= NUM_STATICS:
            self.static = 0
        pass
