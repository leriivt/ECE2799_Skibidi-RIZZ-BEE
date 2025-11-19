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

colors = {
    OFF : (0 ,0, 0),
    RED : (255, 0, 0),
    ORANGE : (255, 128, 0),
    YELLOW : (255, 255, 51),
    GREEN : (51, 255, 51),
    BLUE : (0, 128, 255),
    PURPLE : (153, 51, 255),
    PINK : (255, 51, 153),
    RAINBOW : (128, 128, 128)
}

class LEDController:
    
    def __init__(self, pattern=RED, static=1):
        self.pattern = pattern
        self.static = static
        self.num_pixels = 3
        
        self.pixels = neopixel.NeoPixel(board.GP0, self.num_pixels) #note was GP22
        self.pixels.brightness = 0.5
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
        
    def update_pattern(self):
        if self.static:
            self.pixels.fill(colors[self.pattern])
        else:
            pass
        pass

