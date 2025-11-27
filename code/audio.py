import board
import digitalio
import time

#audio out
import audiocore
from audiopwmio import PWMAudioOut as AudioOut
import adafruit_wave
import audiodelay

#microphone
import pio_i2s

#pitch shifting

from audiobusio import I2SOut
from audiocore import RawSample
from audiodelays import PitchShift
from audiomixer import Mixer


# Audio Ssettings
# SAMPLE_RATE = 48000
# BUFFER_SIZE = 1024
BUFFER_SIZE = 512

properties = {  # These properties will be shared with audioeffects objects
    "buffer_size": BUFFER_SIZE, #try buffer size = 1024
    "sample_rate": 16000, # Reduced sample rate to save memory
    "channel_count": 1,
    "bits_per_sample": 16,
    "samples_signed": True,
}



class AudioController:
    def __init__(self):
        #Initialize audio input/output components
        self.speaker = digitalio.DigitalInOut(board.GP2)
        self.audio = AudioOut(board.A0)

        self.mic = pio_i2s.I2S(
        bit_clock=board.GP3,
        word_select=board.GP4,
        data_in=board.GP1,
        **properties
        )

        self.path = "/sd/kpop.wav" #initial path set to kpop song
        self.recording = False
        self.wav_file = None

        self.times_called = 0 #for toggle_song

        #pitch shifting
        self.pitchshift = PitchShift(
                mix=1.0,
                window=BUFFER_SIZE,
                overlap=max(BUFFER_SIZE>>3, 64),
                **properties,
            )
        
        self.in_buf = bytearray(BUFFER_SIZE * 2)   # 16-bit mono 
        self.out_buf = bytearray(BUFFER_SIZE * 2) 
        self.out_sample = RawSample(self.out_buf, 
                               sample_rate=properties["sample_rate"]) 

        self.buffer_count = 0
    
        
    #problems: real-time pitch shifting will be difficult: each buffer ~60ms,
    # pitch shifting each buffer will sound bad and will make 'clicking' noise
        #   options: 
        #           save different pitch shifted audio files and play each one based on imu data
        #           pitch shift audio every second using a counter


    def process_audio(self, imu_val): #assume imu_val > 3 -> flying
        
        if(3<imu_val<5):
            self.pitchshift.semitones = -12 #pitchshift down 1 octave
        
        elif(5<imu_val<7):
            self.pitchshift.semitones = 0 #no pitch shift
        
        elif(7<imu_val<9):
            self.pitchshift.semitones = 6 #pitch shift up 1/2 octave
        
        elif(9<= imu_val <= 10):
            self.pitchshift.semitones = 12 # pitch shift up 1 octave
        

    def play_audio(self, imu, led):

        with open(self.path, "rb") as f:
            wave = adafruit_wave.open(f)

            while True:

                imu_val = imu.read_acceleration()
                #led.do_led_shit()

                # only update pitch about once per second
                if self.buffer_count % 32 == 0:
                    self.pitchshift(imu_val)

                data = wave.readframes(BUFFER_SIZE)
                if not data:
                    print("Error in reading data")
                    break

                self.in_buf[:len(data)] = data

                # always pitch shift the chunk
                self.pitchshift.render(self.in_buf, self.out_buf)

                self.audio.play(self.out_sample, loop=False)

                while self.audio.playing:
                    pass

                self.buffer_count += 1

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

            if(self.times_called % 2):
                self.path = "/sd/user.wav"
            else:
                self.path = "/sd/kpop.wav"
      


