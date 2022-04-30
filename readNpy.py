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
    wave = np.load(f'Data/npy/{i:06d}.npy')
    plt.plot(wave)
    plt.show()
    i+=1