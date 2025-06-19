import csv
import matplotlib.pyplot as plt
import os
from glob import glob
from datetime import datetime

# Find the two most recently saved CSV files in the current directory
csv_files = sorted(
    glob("*.csv"),
    key=os.path.getmtime,
    reverse=True
)

if len(csv_files) < 2:
    raise FileNotFoundError("Not enough CSV files found in the current directory.")

file1, file2 = csv_files[0], csv_files[1]

# Read data from both CSV files, skipping the header
with open(file1, newline='') as f1, open(file2, newline='') as f2:
    reader1 = list(csv.reader(f1))
    reader2 = list(csv.reader(f2))

header1 = reader1[0]
header2 = reader2[0]
data1 = reader1[1:]
data2 = reader2[1:]

# Convert to dictionaries for fast lookup (frequency as key)
dict1 = {float(row[0]): float(row[1]) for row in data1}
dict2 = {float(row[0]): float(row[1]) for row in data2}

# Find common frequencies
common_freqs = sorted(set(dict1.keys()) & set(dict2.keys()))

# Calculate magnitude differences at each common frequency
diffs = [dict1[f] - dict2[f] for f in common_freqs]

# Generate a unique output file name using date and time
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_file = f'difference_fourier_{timestamp}.csv'

with open(output_file, 'w', newline='') as fout:
    writer = csv.writer(fout)
    writer.writerow(['Frequency (Hz)', 'Magnitude Difference'])
    for freq, diff in zip(common_freqs, diffs):
        writer.writerow([freq, diff])

# Plot the difference
plt.figure(figsize=(10, 6))
plt.plot(common_freqs, diffs)
plt.title('Difference in Magnitude Between Two Fourier Analyses')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude Difference (relative units)')
plt.grid()
plt.xlim(0, 2000)