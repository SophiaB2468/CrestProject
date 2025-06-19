import sounddevice as sd
from scipy.io.wavfile import write
import datetime

fs = 44100  # Sample rate (samples per second)
seconds = 5  # Duration of recording

# Create a unique filename using the current date and time
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"output_{timestamp}.wav"

print("Recording...")
recording = sd.rec(int(seconds * fs), samplerate=fs, channels=1, dtype='int16')
sd.wait()  # Wait until recording is finished
print("Recording finished.")

write(filename, fs, recording)  # Save as WAV file
print(f"Saved as {filename}")