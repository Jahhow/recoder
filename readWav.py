import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
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

i=47
while True:
    samplerate, wave = wavfile.read(f'Data/wav/{i:06d}.wav')
    print('samplerate:',samplerate, ', wave.shape:',wave.shape)
    plt.plot(wave[:1000])
    plt.show()
    i+=1