import csv
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('seaborn')

FRAME_RATE = 48000
FFT_SIZE = 2048
FRAME_STEP = 148
def plotFFT(fft_sample, vmin=None, vmax=None, title=None):
    plt.figure(dpi=60, figsize=(10,5), facecolor='w')
    plt.title(title)
    plt.grid(False)
    plt.pcolormesh(
        np.arange(0, FRAME_RATE/2+FRAME_RATE/FFT_SIZE, FRAME_RATE/FFT_SIZE)[:-1],
        np.arange(0, len(fft_sample)*FRAME_STEP/FRAME_RATE, FRAME_STEP/FRAME_RATE),
        fft_sample, vmin=vmin, vmax=vmax)
    plt.xlabel('Frequency (hz)')
    plt.ylabel('Time (sec)')
    plt.show()

i=0
while True:
    with open(f'csv/{i:06d}.csv', newline='') as f:
        reader = csv.reader(f)
        fft_samples = np.array(list(reader), dtype=np.float32)
        print('shape',fft_samples.shape)
        plotFFT(fft_samples)
    i+=1