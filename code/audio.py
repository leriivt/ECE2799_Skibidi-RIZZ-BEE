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
    



class AudioController:
    def __init__(self):
        #Initialize audio input/output components
        self.speaker = digitalio.DigitalInOut(board.GP2)
        self.audio = AudioOut(board.A0)

        self.mic = pio_i2s.I2S(
        bit_clock=board.GP3,
        word_select=board.GP4,
        data_in=board.GP1,
        channel_count=1,
        sample_rate=16000,  # Reduced sample rate to save memory
        bits_per_sample=16,
        samples_signed=True,
        buffer_size=2048
    )
        self.path = "/sd/kpop.wav" #initial path set to kpop song
        self.recording = False
        self.wav_file = None

        self.times_called = 0 #for toggle_song
    
        
        
    def process_audio(self):
        #Process audio input and apply effects

        #pitch shift audio

        pass

    def play_audio(self, imu_val):

        

        with open(self.path, "rb") as f:
            wave = adafruit_wave.open(f)
            self.audio.play(wave)

            # Wait until playback is finished
            while self.audio.playing:

                time.sleep(0.01)  # short sleep to avoid busy-waiting


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

        

        pass

    def record_audio(self): #save audio as "/sd/user.wav"

        """
        Call this frequently (e.g., every main loop iteration)
        while recording is True. It reads a buffer from the mic
        and appends it to the WAV file.
        """
        if not self.recording:
            return

        try:
            # Read one buffer from the mic and write it
            data = self.mic.read()  # or readinto, depending on your pio_i2s implementation
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
      


