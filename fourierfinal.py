import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt
import glob
import os
import csv

# Find the most recently saved .wav file
wav_files = glob.glob("output_*.wav")
if not wav_files:
    raise FileNotFoundError("No output_*.wav files found in the current directory.")

latest_file = max(wav_files, key=os.path.getctime)

# Read the WAV file
sample_rate, data = wavfile.read(latest_file)

# If stereo, take one channel
if len(data.shape) > 1:
    data = data[:, 0]

# Normalize data to range [-1, 1] for amplitude in relative units
if data.dtype == np.int16:
    data = data / 32768.0
elif data.dtype == np.int32:
    data = data / 2147483648.0
elif data.dtype == np.uint8:
    data = (data - 128) / 128.0

# Perform Fourier Transform
fft_data = np.fft.fft(data)
frequencies = np.fft.fftfreq(len(fft_data), 1 / sample_rate)

# Only plot the positive frequencies
positive_freqs = frequencies[:len(frequencies)//2]
magnitude = np.abs(fft_data)[:len(frequencies)//2]

# Save analysis as CSV
csv_filename = latest_file.replace('.wav', '_fourier.csv')
with open(csv_filename, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Frequency (Hz)', 'Magnitude (relative units)'])
    for freq, mag in zip(positive_freqs, magnitude):
        if 0 <= freq <= 2000:  # Only save up to 2000 Hz as in the plot
            writer.writerow([freq, mag])

plt.figure(figsize=(10, 6))
plt.plot(positive_freqs, magnitude)
plt.title(f'Frequency Spectrum of {latest_file}')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude (relative units)')
plt.xlim(0, 2000)  # Limit x-axis from 0 to 2,000 Hz
plt.ylim(0)        # Start y-axis from zero
plt.grid()
plt.show()