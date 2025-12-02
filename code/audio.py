import board
import digitalio
import time
from LEDs import *
from motion_detection import *

#audio out
import audiocore
from audiopwmio import PWMAudioOut as AudioOut
import adafruit_wave 
from audiocore import WaveFile

# import audiodelays


#microphone
import pio_i2s

#pitch shifting
from audiobusio import I2SOut
from audiocore import RawSample
from audiodelays import PitchShift

# Audio Ssettings
# SAMPLE_RATE = 48000
# BUFFER_SIZE = 1024
BUFFER_SIZE = 512

properties = {  # These properties will be shared with audioeffects objects
    "buffer_size": BUFFER_SIZE, #try buffer size = 1024
    "sample_rate": 24000, # Found 24kHz works best for wav file
    "channel_count": 1,
    "bits_per_sample": 16,
    "samples_signed": True,
}



class AudioController:
    def __init__(self):
        #Initialize audio input/output components
        self.audio = AudioOut(board.GP4)
        self.sd = digitalio.DigitalInOut(board.GP2)
        self.sd.direction = digitalio.Direction.OUTPUT

        self.mic = pio_i2s.I2S(
        bit_clock=board.GP14,
        word_select=board.GP15,
        data_in=board.GP13,
        **properties
        )

        self.path = "/sd/kpop.wav" #initial path set to kpop song
        self.recording = False
        self.wav_file = "/sd/user.wav"
    

        self.times_called = 0 #for toggle_song

        #pitch shifting
        self.pitchshift = PitchShift(
                mix=1.0,
                window=BUFFER_SIZE,
                overlap=max(BUFFER_SIZE>>3, 64),
                **properties,
            )
        
        self.stop_audio = False


    def process_audio(self, imu_val): #assume imu_val > 3 -> flying
        shift = imu_val - 13 #shift imu_val from 1-25 to -12 to 12
        self.pitchshift.semitones = shift 

        

    def play_audio(self, imu, led):

        if(self.stop_audio == False):

            try:
                f = open(self.path, "rb")

                wave = WaveFile(f)
                print("sample_rate:", wave.sample_rate, "channels:", wave.channel_count)
                print("Playing...")
                
                self.pitchshift.semitones = 0
                
                while not imu.detect_catch():
                    
                    self.pitchshift.play(wave)
                    self.audio.play(self.pitchshift)
                    

                    while self.audio.playing and not imu.detect_catch():
                        time.sleep(.05)

                        #Read imu velocity from 1-25
                        imu_val = imu.read_discrete_velocity(25)

                        #do led shit here
                        self.process_audio(imu_val)
                    
                    
                f.close()

            except Exception as e:
                print("Audio error:", e)
                time.sleep(2)
                
        

    def start_recording(self):

        """Begin recording audio into a WAV file. Non-blocking."""
        if self.recording:
            return  # already recording

        # open file for writing
        self.wav_file = adafruit_wave.open("/sd/user.wav", mode="wb")
        self.wav_file.setframerate(self.mic.sample_rate)
        self.wav_file.setnchannels(self.mic.channel_count)
        self.wav_file.setsampwidth(self.mic.bits_per_sample // 8)

        self.recording = True
        
    def stop_recording(self):

        if not self.recording:
            return
        
        self.mic.deinit()
        # close file so header is finalized
        
        self.wav_file.close()
        self.wav_file = None
        self.recording = False


    def record_audio(self): #save audio as "/sd/user.wav"
        """
        reads a buffer from the mic and appends it to the WAV file.
        """
        if not self.recording:
            return

        try:
            # Read one buffer from the mic and write it
            data = self.mic.read()
            if data:
                self.wav_file.writeframes(data)
        except Exception as e:
            print("Error during recording:", e)
            self.stop_recording()


    def toggle_audio(self): #toggle between microphone recorded audio & Kpop demon hunters
            self.times_called+=1  

            if(self.times_called % 3 == 1):
                self.stop_audio = False
                self.path = "/sd/user.wav"
            elif(self.times_called % 3 == 2):
                self.stop_audio = True
            else:
                self.stop_audio = False
                self.path = "/sd/kpop.wav"

    def speaker_off(self):
        if(self.sd == True):
            pass
        else:
            self.sd = True

    def speaker_on(self):
        if(self.sd == False):
            pass
        else:
            self.sd = False