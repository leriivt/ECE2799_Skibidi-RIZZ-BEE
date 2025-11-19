import board
import digitalio
import time

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
        audio = AudioOut(board.A0)

        wave_file = open("StreetChicken.wav", "rb")
        #wave = WaveFile(wave_file)
        #audio = AudioOut(board.A0)
        
    def process_audio(self, value, file):
        #Process audio input and apply effects

        #pitch shift audio

        pass
    def play_audio(self, mp3file):
        # # You have to specify some mp3 file when creating the decoder
        mp3 = open(mp3file, "rb")
        decoder = MP3Decoder(mp3)
        audio = AudioOut(board.A0)

        
        # Updating the .file property of the existing decoder
        # helps avoid running out of memory (MemoryError exception)
        decoder.file = open(mp3file, "rb")
        audio.play(decoder)
        print("playing", mp3file)

        # This allows you to do other things while the audio plays!
        while audio.playing:
            led.value = True
            time.sleep(0.5)
            led.value = False
            time.sleep(0.5)

       
        
        
        #audio.play(wave)
        pass




# #"""CircuitPython Essentials Audio Out MP3 Example"""

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


