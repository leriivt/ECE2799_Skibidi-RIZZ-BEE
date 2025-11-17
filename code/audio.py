from audiomp3 import MP3Decoder

try:
    from audioio import AudioOut
except ImportError:
    try:
        from audiopwmio import PWMAudioOut as AudioOut
    except ImportError:
        pass  # not always supported by every board!


class AudioController:
    def __init__(self):
        #Initialize audio input/output components
        self.mic = digitalio.DigitalInOut(board.GP16) #Figure out later
        self.speaker = digitalio.DigitalInOut(board.GP2)

        wave_file = open("StreetChicken.wav", "rb")
        #wave = WaveFile(wave_file)
        #audio = AudioOut(board.A0)
        
    def process_audio(self, value):
        #Process audio input and apply effects


        pass
    def play_audio(self):
        
        
        #audio.play(wave)
        pass




# #"""CircuitPython Essentials Audio Out MP3 Example"""
# import board
# import digitalio
# import time
# # import audiopwmio



# button = digitalio.DigitalInOut(board.A1)
# button.switch_to_input(pull=digitalio.Pull.UP)

# led = digitalio.DigitalInOut(board.LED)
# led.direction = digitalio.Direction.OUTPUT


# # The listed mp3files will be played in order
# mp3files = ["Claypigeons.mp3"]

# # You have to specify some mp3 file when creating the decoder
# mp3 = open(mp3files[0], "rb")
# decoder = MP3Decoder(mp3)
# audio = AudioOut(board.A0)

# while True:
#     for filename in mp3files:


#         # Updating the .file property of the existing decoder
#         # helps avoid running out of memory (MemoryError exception)
#         decoder.file = open(filename, "rb")
#         audio.play(decoder)
#         print("playing", filename)

#         # This allows you to do other things while the audio plays!
#         while audio.playing:
#             led.value = True
#             time.sleep(0.5)
#             led.value = False
#             time.sleep(0.5)

#         print("Waiting for button press to continue!")
#         while button.value:
#             pass


